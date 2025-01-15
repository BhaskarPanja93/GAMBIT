from os import listdir
from pathlib import Path
from random import shuffle
from threading import Thread
from time import sleep, time
from wave import open

from OtherClasses.Folders import Folders


class MusicStream:
    def __init__(self, fileName, category, onCompleteCallback):
        self.closed = False
        self.onCompleteCallback = onCompleteCallback
        self.category = category
        self.fileName = fileName
        self.partsPerSecond = 10
        self.wf = open(self.fileName, 'rb')
        self.sampleRate = self.wf.getframerate()
        self.chunkSize = self.sampleRate // self.partsPerSecond
        self.chunkTime = 1 / self.partsPerSecond
        self.currentChunkStartTime = 0
        self.currentChunk = b""
        self.currentChunkIndex = 0
        self.header = self.__createHeader()


    def start(self):
        while not self.closed:
            self.__readNextChunk()


    def __close(self):
        self.closed = True


    def __readNextChunk(self):
        self.currentChunkStartTime = time()
        self.currentChunk = self.wf.readframes(self.chunkSize)
        if not self.currentChunk:
            self.__close()
            return self.onCompleteCallback(self.category, self)
        else: sleep(self.chunkTime)


    def getCurrentChunk(self) -> bytes:
        return self.currentChunk


    def __createHeader(self):
        channels = 2
        bitsPerSample = 16
        sampleRate = self.wf.getframerate()
        datasize = 2000 * 10 ** 6
        return (bytes("RIFF", 'ascii')
        + (datasize + 36).to_bytes(4, 'little')
        + bytes("WAVE", 'ascii')
        + bytes("fmt ", 'ascii')
        + (16).to_bytes(4, 'little')
        + (1).to_bytes(2, 'little')
        + channels.to_bytes(2, 'little')
        + sampleRate.to_bytes(4, 'little')
        + (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')
        + (channels * bitsPerSample // 8).to_bytes(2, 'little')
        + bitsPerSample.to_bytes(2, 'little')
        + bytes("data", 'ascii')
        + datasize.to_bytes(4, 'little'))


class MusicCollection:
    def __init__(self):
        self.activeStreams:dict[str,MusicStream] = {}
        self.files:dict[str, list[str]] = {}
        for cat in listdir(Folders.music):
            cat = str(cat)
            categoryFolder = Path(Folders.music) / cat
            if categoryFolder.is_dir():
                self.files[cat] = []
                for fileName in listdir(categoryFolder):
                    fileName = Path(categoryFolder) / fileName
                    if fileName.is_file():
                        self.files[cat].append(str(fileName))
                if not self.files[cat]:
                    self.files.pop(cat)
                    continue
                else:
                    shuffle(self.files[cat])
                    Thread(target=self.startNextFile, args=(cat, None,)).start()


    def startNextFile(self, category:str, stream: MusicStream | None):
        sleep(1)
        if stream is not None: self.files[category].append(stream.fileName)
        self.activeStreams[category] = MusicStream(self.files[category].pop(0), category, self.startNextFile)
        self.activeStreams[category].start()


    def getStream(self, category:str):
        return self.activeStreams.get(category)
