import zstandard as zstd
from PIL import Image
from struct import pack as pk, unpack as up
import os

# Based on asset extraction script by SciresM, who did all the work
# figuring out the asset format and encryption.
#
# Here is my modified version of his script that you can use to extract all assets:
# https://gist.github.com/Cloppershy/a32b9139f3d222b5ff5b8b23ffac1aac

# * You need Python 2, pip install zstandard Pillow.
# * Copy the original Spel2.exe and name it Spel2-orig.exe
# * Create a folder Mod and put any assets in there that you want to replace
#   (with the same folder structure inside, e.g. Data/Textures/). You don't
#   need to (and shouldn't) put any unmodified assets in there.
#   Textures (.png files) are read from the Mod folder as actual PNG files,
#   you do not need to convert them into raw RGBA arrays.
# * Run spelunky2_mod.py, it will create Spel2-modded.exe that contains the
#   modified assets and has the asset checksum patched out.
# * Replace your Spel2.exe with Spel2-modded.exe and run the game.
#
# Currently each modified asset has to be the same size or smaller than the
# original asset for this to work. This shouldn't be a problem, since the assets
# are stored compressed and you can just up the compression factor. It's set to
# 16 in the script, which is already higher than the one used originally, but
# you can increase it up to 22 if your assets are too big.

GAME_PATH = "Spel2-orig.exe"  # Unmodified game
ASSET_DIR = "Mod"  # Folder containing modified assets. Must have same structure as extracted assets
OUTPUT = "Spel2-modded.exe"  # Output file

COMPRESSION_LEVEL = 16  # Value between 1 and 22 (higher = smaller data size) - if modified assets are too large, increase compression
KEEP_CONVERTED_RAW_IMAGES = False  # Keep .png.raw files with RGBA array after conversion (for debug purposes only)
DEBUG_LIST_ASSETS = False  # Lists all asset offsets while scanning the original game binary



class Asset:
    def __init__(self, offset, name_len, asset_len,
                 name_hash, encrypted, data_offset, data_size):
        self.offset = offset
        self.name_len = name_len
        self.asset_len = asset_len

        self.name_hash = name_hash
        self.encrypted = encrypted
        self.data_offset = data_offset
        self.data_size = data_size

    @property
    def total_size(self):
        return 8 + self.name_len + self.asset_len

    def match_hash(self, hash):
        l = min(len(hash), self.name_len)
        return hash[:l] == self.name_hash[:l]

    @staticmethod
    def from_bytes(bytes, offset):
        asset_len, name_len = up('<II', bytes[offset:offset+8])
        if asset_len == 0 and name_len == 0:
            return None
        assert asset_len >= 1

        asset = Asset(
            offset, name_len, asset_len,
            bytes[offset+8:offset+8+name_len],
            bytes[offset+8+name_len] in (1, '\x01'),
            offset + 8 + name_len + 1,
            asset_len - 1
        )
        return asset


class AssetLibrary:
    START_OFFSET = 0x400  # Start offset for asset data in Spel2.exe

    # Instructions for asset checksum check to be patched out
    PATCH_INSTRUCTIONS = "\x33\xC9\xFF\x15\x05\x13\x2F\x00\xCC"
    NOP = "\x90" * len(PATCH_INSTRUCTIONS)

    def __init__(self, bytes):
        self.bytes = bytearray(bytes)

        self.assets = []
        self.analyse_bytes()
        self.patch()

    def analyse_bytes(self):
        self.assets[:] = []  # Python 2 .clear()

        print("Listing assets")
        ofs = self.START_OFFSET
        while True:
            asset = Asset.from_bytes(self.bytes, ofs)
            if asset is None:
                break
            self.assets.append(asset)
            if DEBUG_LIST_ASSETS:
                print("Asset at 0x{:08x}, total size 0x{:08x} (8 + 0x{:04x} + 0x{:08x})".format(asset.offset, asset.total_size, asset.name_len, asset.asset_len))
            ofs += asset.total_size
        if DEBUG_LIST_ASSETS:
            print("End at {:08x}".format(ofs))
        print("Found {} assets".format(len(self.assets)))

    def patch(self):
        # Patch out checksum check for asset loading
        print("Patching asset checksum check")
        index = self.bytes.find(self.PATCH_INSTRUCTIONS)
        if index == -1:
            print("Didn't find instructions to patch. Is game unmodified?")
            return False

        print("Found check at 0x{:08x}, replacing with NOPs".format(index))
        self.bytes[index:index+len(self.NOP)] = self.NOP

    @staticmethod
    def load_from_file(path):
        print("Reading game binary from \"{}\"".format(path))
        with open(path, 'rb') as f:
            exe = f.read()
        return AssetLibrary(exe)

    def write_to_file(self, path):
        print("Writing modified game binary to \"{}\"".format(path))
        with open(path, 'wb') as f:
            f.write(self.bytes)

    def find_asset(self, name):
        name_hash = filename_hash(name)
        for asset in self.assets:
            if asset.match_hash(name_hash):
                return asset
        return None

    def replace_asset(self, name, new_data):
        asset = self.find_asset(name)

        if asset is None:
            print("Asset \"{}\" was not found in the game file and could not be replaced".format(name))
            return False

        if asset.encrypted:
            size_raw = len(new_data)
            new_data = encrypt_data(name, new_data)
            print("Encrypting data for \"{}\" ({} bytes -> {} bytes)".format(name, size_raw, len(new_data)))

        old_size = asset.data_size
        new_size = len(new_data)

        if new_size > old_size:
            print("Asset \"{}\" is larger than original ({} bytes > {} bytes), replacing currently not possible".format(name, new_size, old_size))
            return False

        if new_size == old_size:
            print("Replacing asset \"{}\" with same size ({} bytes)".format(name, new_size))
            self.bytes[asset.data_offset:asset.data_offset+new_size] = new_data

        if new_size < old_size:
            print("Replacing asset \"{}\" with smaller size ({} bytes < {} bytes)".format(name, new_size, old_size))
            self.bytes[asset.data_offset:asset.data_offset+new_size] = new_data

            diff = old_size - new_size
            if diff < 10:
                print("Difference is less than 10 bytes, not enoguh space to insert a padding asset. Things might break")
            else:
                # Old/Replaced asset size
                self.bytes[asset.offset:asset.offset+4] = pk("<I", new_size + 1)
                # New padding asset size (with name_len = 1)
                self.bytes[asset.data_offset+new_size:asset.data_offset+new_size+8] = pk("<II", diff - 9, 1)

        return True

def main():
    library = AssetLibrary.load_from_file(GAME_PATH)

    count_replaced = 0
    count_failed = 0
    for dir, subdirs, files in os.walk(ASSET_DIR):
        for file in files:
            filepath = os.path.join(dir, file)
            name = filepath.replace(ASSET_DIR, "").replace("\\", "/")[1:]

            if name.endswith(".png.raw"):
                continue  # skip converted images
            elif name.endswith(".png"):
                print("\nConverting image \"{}\" to RGBA array".format(name))
                img = Image.open(filepath).convert('RGBA')
                new_data = pk('<II', img.width, img.height) + b_to_s([
                    (byte if rgba[3] != 0 else 0)  # Hack to force all transparent pixels to be (0, 0, 0, 0) instead of (255, 255, 255, 0)
                    for rgba in img.getdata()
                    for byte in rgba
                ])
                if KEEP_CONVERTED_RAW_IMAGES:
                    with open(filepath + ".raw", 'wb') as f:
                        f.write(new_data)
            else:
                print("")
                with open(filepath, 'rb') as f:
                    new_data = f.read()

            if library.replace_asset(name, new_data):
                count_replaced += 1
            else:
                count_failed += 1

    print("")
    print("Successfully replaced {} files, {} errros".format(count_replaced, count_failed))
    library.write_to_file(OUTPUT)

if __name__ == '__main__':
    main()
