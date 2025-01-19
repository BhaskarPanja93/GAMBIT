from os import listdir, stat
from pathlib import Path
from random import shuffle
from subprocess import Popen, PIPE, DEVNULL
from threading import Thread, Condition
from time import sleep
from pydub import AudioSegment


from OtherClasses.Folders import Folders


class MusicStreamCategory:
    def __init__(self, category, folderPath: Path):
        self.closed = False
        self.category = category
        self.folderPath = folderPath
        self.lastFolderModification = 0
        self.files:list[Path] = []
        self.currentFilePath: Path | None = None
        self.allChunks:list[bytes] = []
        self.condition = Condition()
        self.process = None


    def kill(self):
        self.closed = True


    def spawn(self):
        self.__reReadFiles()
        Thread(target=self.__nextFile).start()
        Thread(target=self.__listenToFileChanges).start()


    def __listenToFileChanges(self):
        while (not self.closed) and self.folderPath.exists():
            current = stat(self.folderPath).st_mtime
            if current != self.lastFolderModification:
                self.lastFolderModification = current
                self.__reReadFiles()
            sleep(2)


    def __reReadFiles(self):
        self.files = []
        for fileName in listdir(self.folderPath):
            filePath = self.folderPath / fileName
            if filePath.is_file():
                self.files.append(filePath)
        shuffle(self.files)


    def __nextFile(self):
        if self.closed: return
        if self.currentFilePath is not None: self.files.append(self.currentFilePath)
        if not self.files:
            print(f"Waiting for music files in {self.category}")
            while (not self.files) and (not self.closed): sleep(1)
        if self.closed: return
        self.currentFilePath = self.files.pop(0)
        print(f"{self.category}: {self.currentFilePath}")
        Thread(target=self.__startListening).start()


    def __startListening(self):
        chunkSize = 1024
        _mp3 = AudioSegment.from_mp3(self.currentFilePath)
        frameRate = _mp3.frame_rate
        self.process = Popen(
            ['ffmpeg', '-re', '-i', str(self.currentFilePath), "-f", "mp3", "-"],
            stdout=PIPE,
            stderr=DEVNULL
        )
        while not self.closed:
            data = self.process.stdout.read(chunkSize)
            if not data: break
            self.allChunks.append(data)
            if len(self.allChunks) > 8*frameRate/chunkSize:
                with self.condition:
                    self.allChunks.pop(0)
                    self.condition.notify_all()
        self.process.stdout.close()
        self.process.kill()
        self.process.wait()
        Thread(target=self.__nextFile).start()


class MusicCollection:
    def __init__(self):
        self.closed = False
        self.activeStreams:dict[str,MusicStreamCategory] = {}
        self.lastFolderModification = 0
        Thread(target=self.__listenToFolderChanges).start()


    def __listenToFolderChanges(self):
        while not self.closed:
            current = stat(Folders.music).st_mtime
            if current != self.lastFolderModification:
                self.lastFolderModification = current
                self.generateStreams()
            sleep(2)


    def generateStreams(self):
        currentFolders = listdir(Folders.music)
        currentStreams = list(self.activeStreams)
        for catName in currentFolders:
            catPath = Folders.music / catName
            if catPath.is_dir():
                if catName not in self.activeStreams:
                    self.activeStreams[catName] = MusicStreamCategory(catName, catPath)
                    print(f"Spawned {catName}")
                    self.activeStreams[catName].spawn()

        for catName in currentStreams:
            if catName not in currentFolders:
                print(f"Killed {catName}")
                self.activeStreams.pop(catName).kill()


    def close(self):
        for stream in self.activeStreams.values():
            stream.kill()
        print("Music Collection Stopped")
