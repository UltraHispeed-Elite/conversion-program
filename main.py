import os 
import json

#template code

#phase one, creates the directories if they don't already exist
def makemydir(whatever):
  try:
    os.makedirs(whatever)
  except OSError:
    print(whatever+" already exists")
    pass

#phase two, lists all behavior and resource packs that need to be converted
def list_items(dir):
    # Get the list of all files and directories
    path = dir
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")
    # prints all files
    print(dir_list)
    return dir_list

#phase three, creates new directories based on the data and asset lists
def output_files(name, type):
  makemydir("outputs/"+name)

  newDir = "outputs/"+name

  if type == "data":
    makemydir(newDir+"/data")
    makemydir(newDir+"/data/fabricaddons")
  elif type == "asset":
    makemydir(newDir+"/assets")
    makemydir(newDir+"/assets/fabricaddons")

#phase four
template = {
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": 0
  }
}

def modelConv(texture_source, output_id):
    f = open(texture_source, "r")

    test = f.read()

    data = json.loads(test)

    print(data)

    textures = data['texture_data']

    for item in textures:
        print(item)
        
        model = template
        
        name = item.split(".")
        new_name = name[1]
        
        print(name)
        
        item_id = textures[item]["textures"]
        split_id = item_id.split("/")
        print(split_id)
        new_id = split_id[1]+"/"+split_id[2]
        
        f.close()

        makemydir("outputs/"+output_id+"/assets/fabricaddons/model/item")
        f = open("outputs/"+output_id+"/assets/fabricaddons/model/item/"+new_name+".json", "w")

        model["textures"]["layer0"] = name[0]+":"+new_id
        
        f.write(json.dumps(model))

#outputting phase one
makemydir("resource_packs")
makemydir("behavior_packs")
makemydir("outputs")

#outputting phase two
data_list = list_items("behavior_packs")
asset_list = list_items("resource_packs")


print(asset_list, data_list)

#outputting phase three
for item in data_list:
  output_files(item, "data")

for item in asset_list:
  output_files(item, "asset")

for i in asset_list:
  modelConv("resource_packs/"+i+"/textures/item_texture.json", i)
