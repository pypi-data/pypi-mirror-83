from cement import Controller, ex, shell
from cement.utils import fs
from PIL import Image
from astropy.io import fits
import numpy
import exifread
import sys
import os
import csv

class Convert(Controller):
    class Meta:
        label = 'convert'
        stacked_type = 'embedded'
        stack_on = 'base'

    @ex(help='convert single image to specified format')
    def convert_img(self):
        available_formats = {
            'tif': ['fits', 'csv'],
            'tiff': ['fits', 'csv']
        }

        def input_file():
            x = shell.Prompt("What is the name of the file you would like to convert?")
            xres = x.prompt()
            input_format = xres.rsplit('.', 1)[1]
            if input_format in available_formats.keys():
                return output_file(input_format, xres)
            else:
                print("The entered format is not currently supported by letsformat.\n")
                return input_file()

        def output_file(input_format, file):
            print(f"Currently supported output formats for {input_format} are {available_formats[input_format]}\n")
            x = shell.Prompt("What format would you like to convert this file to?")
            xres = x.prompt()
            output_format = xres.rsplit('.', 0)[0]
            if output_format in available_formats[input_format]:
                return get_directory(input_format, output_format, file)
            else:
                print("The entered format conversion is not currently supported by letsformat\n")
                return output_file(input_format, file)
        
        def get_directory(input_format, output_format, file):
            file_dir = ""
            x = shell.Prompt("What is the path of your file located in? (Press Enter for Current Working Directory)",
                             default='ENTER')
            xres = x.prompt()
            if xres == 'ENTER':
                file_dir = fs.join(fs.abspath(os.getcwd()), file)
            else:
                file_dir = fs.join(fs.abspath(xres), file)
            if file_dir:
                metadata = input_file_metadata(input_format, file_dir)
                image_data = input_file_image_data(input_format, file_dir)
                return process_picture(metadata, image_data, output_format, input_format, file_dir)
            else:
                return get_directory(input_format, output_format, file)

        def input_file_metadata(input_format, path):
            if input_format == 'tif' or input_format == 'tiff' or input_format == 'jpg':
                return exifread.process_file(open(path, 'rb'))

        def input_file_image_data(input_format, path):
            img = Image.open(path)
            return numpy.array(img)

        def process_picture(metadata, image_data, output_format, input_format, path):
            if output_format == 'fits':
                return write_to_fits(metadata, image_data, input_format, path)
            elif output_format == 'csv':
                return write_to_csv(metadata, path)

        def write_to_fits(metadata, image_data, input_format, path):
            primary_header = fits.Header()
            primary_hdu = fits.PrimaryHDU(header=primary_header)
            for data in metadata:
               my_key = []
               my_val = []
               for char in str(metadata[data]):
                   if ord(char) > 32 and ord(char) < 126:
                       my_key.append(char)
               for char in data:
                   if ord(char) > 32 and ord(char) < 126:
                       my_val.append(char)
               primary_header[''.join(my_val)[0:7]] = ''.join(my_key)
            image_hdu = fits.ImageHDU(image_data)
            hdul = fits.HDUList([primary_hdu, image_hdu])
            hdul.writeto('test.fits')
            checkme = fits.open('test.fits')
            checkme.info()

        def write_to_csv(metadata, path):
            csv_cols = []
            for key in metadata:
                csv_cols.append(key)
            try:
                with open(path + ".csv", "w") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
                    writer.writeheader()
                    writer.writerow(metadata)
            except IOError:
                print("I/O Error")

        p = shell.Prompt("Currently Supported image formats are .tif(tiff)\nPress Enter to Continue",
                         default='ENTER')
        res = p.prompt()
        input_file()
