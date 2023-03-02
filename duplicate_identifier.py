import csv

header = []
rows = []

# Load the metadata
with open('./collection/metadata.csv', newline='') as csvfile:
    metadata = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in metadata:
        if (row[0] == 'File'): #ignore the header
            header = row
        else:
            rows.append(row)

# This file will contain all of the duplicates located
f = open('./identified_duplicates.csv', 'w', newline='')
writer = csv.writer(f, delimiter =';')
writer.writerow(header)

images_with_duplicates = 0
images_requiring_reassignment = 0
duplicate_traits_identified = []

# Quick and dirty nested loop.
# This is bad time efficiency O <= n^2
# But will do for a quick turn solution
for x in range(len(rows)) :
    duplicate_located_for_x = False
    
    this_traits = []
    for trait in rows[x][3:]:
        this_traits.append(trait)

    if (not (this_traits in duplicate_traits_identified)):
        # Compare this row against the rest of the rows
        for y in range(len(rows) - x - 1):
            other = y + x + 1

            other_traits = []
            
            for trait in rows[other][3:]:
                other_traits.append(trait)
            
            if (this_traits == other_traits):
                # A duplicate has been located
                if (not duplicate_located_for_x):
                    duplicate_located_for_x = True
                    writer.writerow(rows[x])
                    images_with_duplicates += 1
                
                writer.writerow(rows[other])
                images_requiring_reassignment += 1
        if (duplicate_located_for_x):
            writer.writerow([]) # Leave a space
            duplicate_traits_identified.append(this_traits)
            
f.close()

print("Done")
print(f'Duplicates exist for {images_with_duplicates} NFT\'s')
print(f'Requiring re-assignment of {images_requiring_reassignment} NFT\'s')
print("See identified_duplicates.csv for specifics")
            
        