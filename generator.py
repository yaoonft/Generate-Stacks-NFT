from dataclasses import dataclass
from shutil import rmtree
from os import path, mkdir
from PIL import Image 
import random
import csv

# Change these
TOTAL_IMAGES = 10 # Number of random unique images you want to generate
all_images = [] # This is used to store the images as they are generated
OUTPUT_DIR = f'./collection'

# Each image is made up a series of traits
@dataclass
class Trait:
    name: str
    variants: list[str]
    weights: list[int]

# Each image is made up a series of traits
# Make sure these traits match your component file names
# e.g., 'Pink' for Pink.png
# The weightings for each trait drive the rarity and add up to 100%
# Note traits in this list must be in order of Layer. I.e., Background first, Foreground last.
traits = [
    Trait(
        "Background", 
        ["Blue Sky", "Blue", "Cream", "Green", "Lime", "Pink", "Purple", "Red", "Wheat", "White"],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]), # 30% + 20% + 10% + 40% = 100%
    Trait(
        "Base", 
        ["Alien", "Blue Soul", "Blues", "Brown", "Dark", "Gold", "Monster", "Orange", "Pinks", "Purples", "Reds", "Whites", "Zombie"], 
        [5, 5, 10, 10, 5, 5, 5, 10, 10, 10, 10, 10, 5]),
    Trait(
        "Eyes", 
        ["Angry", "Bored Eye", "Closed", "Happy Eye", "Looking Left", "Looking Top", "Normal Eye", "Sad", "Shock", "Wink"], 
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]),
    Trait(
        "Mouth", 
        ["Angry Mouth", "Balloon", "Bored", "Chia Mask", "Cigar", "Fangs", "Happy", "Normal", "Open 2", "Open Mouth", "Sadly", "Smile 2", "Smiles", "Smoke", "Tongue"], 
        [10, 5, 5, 10, 5, 10, 5, 5, 10, 10, 5, 5, 5, 5, 5]),
    Trait(
        "Cloth", 
        ["Banana Shirt", "Basketball", "Black Shirt", "Blue Hoodie", "Blue Shirt Bag", "Blue Tie", "Bow", "Camera", "Chef", "Chia Costume", "Clear Cloth", "Dexie","FMB","Jail","Mermaid Costume","Mummy Costume", "Naruto Hoodie", "Paint Shirt", "Purple Shirt","Red Cloth","Red Tie", "Sweater", "Torn Shirt", "Yellow Hoodie"], 
        [3, 3, 5, 5, 5, 5, 5, 5, 5, 2, 5, 2, 5, 5, 5, 5, 5, 2, 2, 5, 5, 5, 3, 3]),
    Trait(
        "Eyewear", 
        ["3D Glasses", "Blindfold", "Clear", "Green Glasses", "Invisible Glasses", "Pirate Glasses", "Pixel Glasses", "Ski Glasses", "Sunglasses", "Visor", "VR"], 
        [10, 10, 10, 5, 10, 10, 10, 10, 10, 10, 5]),
    Trait(
        "Headwear", 
        ["Army Hat", "Arrow", "Artist Hat", "Banana", "Blue Backwards", "Camera Bandana", "Chia Bandana", "Clear Hat", "Cowboy", "Crown", "Devil Horn", "Egg","Fishing Hat","Golf Hat","halo","Headband", "Headphone", "Jeans Hat", "Ninja","Octopus","Pencil Bandana", "Pirate", "Pizza", "Police", "Purple Backwards", "Rainbow Hat", "Red Beanie", "Sailor Hat", "Samurai", "Santa", "Sheep Hat", "Straw Hat", "Toilet Paper", "XCH Hat", "Yellow Beanie"], 
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]),
]

## For a Simple project you should only need to change values above this line

## Generate Traits
# A recursive function to generate unique image combinations
def create_new_image():
    new_image = {}
    
    # For each trait category, select a random trait based on the weightings
    for trait in traits:
        new_image[trait.name] = random.choices(trait.variants, trait.weights)[0]
    
    if (new_image in all_images):
        return create_new_image()
    else:
        return new_image



## Helper function for generating progress bars    
# Print iterations progress
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#', printEnd = "\r"):
    total = len(iterable)
    
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        
    # Initial Call
    printProgressBar(0)
    
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
        
    # Print New Line on Complete
    print()



# Generate the unique combinations based on trait weightings
for i in progressBar(range(TOTAL_IMAGES), prefix = 'Combining Images:', suffix = 'Complete', length = 32):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)
    
    
    
## Check the stats of the new images
# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique? %s" % (all_images_unique(all_images)))


#### Generate Images and Metadata 
for i in range(TOTAL_IMAGES):
    file_data = {
        "File": "%s.PNG" % (str(i + 1))}
    file_data.update(all_images[i])
    all_images[i] = file_data


# Note: Will delete existing files in Output Directory
# This is a feature, for quick re-generation
if path.isdir(OUTPUT_DIR):
    rmtree(OUTPUT_DIR)
mkdir(OUTPUT_DIR)


# Create the metadata.csv
metadata_file = open("./collection/metadata.csv", 'w', newline='')
writer = csv.writer(metadata_file, delimiter =',')

# Write the metadata headers
writer.writerow(all_images[0].keys())

# Create the .png files
for image in progressBar(all_images, prefix = 'Assembling Images & Metadata:', suffix = 'Complete', length = 20):
    layers = []

    # Load each of the Images Layers
    for trait in traits:
        layers.append(Image.open(f'./components/{image[trait.name]}.png').convert('RGBA'))

    # Create the composite
    composite = Image.alpha_composite(layers[0], layers[1])
    for next_layer in layers[2:]:
        composite = Image.alpha_composite(composite, next_layer)

    #Convert to RGB
    rgb_im = composite.convert('RGB')
    rgb_im.save(OUTPUT_DIR + "/" + image["File"])

    # Write the metadata for this item to metadata.csv
    writer.writerow(image.values())

metadata_file.close()

print("Successfully Assembled.\n")