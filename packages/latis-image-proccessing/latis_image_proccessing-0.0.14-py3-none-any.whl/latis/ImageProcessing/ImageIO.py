from .Image import Image
import numpy as np
import gdcm
import pydicom
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000, RLELossless, ImplicitVRLittleEndian

class ImageIO:
    # private
    @staticmethod
    def ensure_even(stream):
        # Very important for some viewers
        if len(stream) % 2:
            return stream + b"\x00"
        return stream


    @staticmethod
    def loadImage(file):
        ds = pydicom.dcmread(file)
        pixel_array = np.uint16(ds.pixel_array)
        cols = ds.Columns
        rows = ds.Rows
        return Image(pixel_array, cols, rows, ds)

    @staticmethod
    def buildFile(image, saveName):
        # TODO : edit height and width elements
        dataset = ImageIO.buildDataSetImplicitVRLittleEndian(image)
        dataset.save_as(saveName)
        return saveName

    @staticmethod
    def buildDataSetJPEG2000(image):
        from io import BytesIO
        from PIL import Image as PImage
        dataset = image.dataset
        pixels = image.pixelData
        frame_data = []
        with BytesIO() as output:
            image = PImage.fromarray(pixels)
            image.save(output, format="JPEG2000")
            frame_data.append(output.getvalue())
        dataset.PixelData = encapsulate(frame_data)
        dataset.file_meta.TransferSyntaxUID = JPEG2000
        dataset.is_implicit_VR = False
        return dataset

    @staticmethod
    def buildDataSetImplicitVRLittleEndian(image):
        dataset = image.dataset
        pixels = image.pixelData
        dataset.PixelData = pixels.tobytes()
        dataset.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
        dataset.is_implicit_VR = True
        return dataset
