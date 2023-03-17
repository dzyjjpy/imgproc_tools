

import os
import shutil
from tqdm import tqdm

root_dir = r"H:\cls_fmg_scene\train_0227"
# root_dir = r"H:\cls_fmg_scene\train_0208"
train_txt = open("train_cornercases_20230227.txt", "w")


scene_classes_dicts_36 = {
    "airport": ["airfield", "heliport"],
    "building": ["apartment_building-outdoor","building_facade","office_building","skyscraper"],
    "bedroom": ["bedchamber", "bedroom", "hotel_room"],
    "basketball_field": ["basketball_court-indoor"],
    "beach": ["beach","coast"],
    "boardwalk": ["boardwalk"],
    "desert": ["desert-sand"],
    "Europe_building": ["palace", "mosque-outdoor","castle","church-outdoor"],
    "flower": ["florist_shop-indoor"],
    "food": ["food","delicatessen","pizzeria"],
    "football_field": ["football_field", "stadium-baseball", "stadium-football", "stadium-soccer"],
    "forest": ["bamboo_forest", "forest-broadleaf", "rainforest"],
    "grass_field": ["farm", "field-cultivated", "golf_course", "pasture"],
    "grotto": ["grotto"],
    "gym": ["gymnasium-indoor"],
    "kitchen": ["kitchen", "galley"],
    "livingroom": ["living_room"],
    "mountain": ["mountain","butte"],
    "ocean": ["ocean","islet","oilrig","wave"],
    "oldtown": ["oldtown"],
    "pagoda": ["pagoda"],
    "path": ["forest_path", "mountain_path"],
    "pavillion": ["gazebo-exterior","pavilion"],
    "park": ["park", "botanical_garden", "formal_garden", "japanese_garden", "topiary_garden"],
    "picnic": ["picnic_area"],
    "porch": ["porch","arcade"],
    "road": ["field_road", "forest_road", "desert_road","highway"],
    "roadtrip": ["roadtrip"],
    "ruin": ["kasbah", "ruin"],
    "snow_field": ["snowfield","mountain_snowy","crevasse"],
    "street": ["street", "crosswalk"],
    "water": ["river", "lake-natural", "moat-water","boathouse","canal-natural","canal-urban"],
    "waterfall": ["waterfall"],
    "wooden_house":["barn","chalet","cottage","hunting_lodge-outdoor"],
    "zen_garden": ["zen_garden"],
    "other": ["airplane_cabin","airport_terminal","amphitheater","amusement_arcade","amusement_park","aquarium","aqueduct","arch","archaelogical_excavation","archive","arena-hockey","arena-performance","army_base","art_gallery","art_school","art_studio","artists_loft","assembly_line","atrium-public","attic","auditorium","auto_factory","auto_showroom","badlands","balcony-interior","ball_pit","ballroom","bank_vault","banquet_hall","bar","barndoor","basement","bathroom","bazaar-indoor","bazaar-outdoor","beauty_salon","beer_hall","biology_laboratory","bookstore","booth-indoor","bowling_alley","boxing_ring","bullring","burial_chamber","bus_interior","bus_station-indoor","cabin-outdoor","candy_store","car_interior","carrousel","catacomb","cemetery","chemistry_lab","church-indoor","classroom","clean_room","closet","clothing_store","cockpit","computer_room","conference_center","conference_room","construction_site","corridor","courtyard","department_store","diner-outdoor","dining_hall","dining_room","discotheque","doorway-outdoor","downtown","dressing_room","drugstore","elevator_lobby","elevator_shaft","elevator-door","engine_room","entrance_hall","escalator-indoor","excavation","fabric_store","fastfood_restaurant","fire_escape","fire_station","flea_market-indoor","food_court","garage-indoor","garage-outdoor","gas_station","general_store-indoor","general_store-outdoor","gift_shop","hangar-indoor","hangar-outdoor","hardware_store","home_office","house","ice_skating_rink-indoor","ice_skating_rink-outdoor","industrial_area","inn-outdoor","jacuzzi-indoor","jail_cell","jewelry_shop","junkyard","kennel-outdoor","kindergarden_classroom","motel","movie_theater-indoor","museum-indoor","music_studio","natural_history_museum","nursing_home","office","office_cubicles","operating_room","orchestra_pit","pantry","parking_garage-indoor","parking_lot","patio","pet_shop","pharmacy","phone_booth","physics_laboratory","playground","playroom","promenade","pub-indoor","railroad_track","reception"]
}

scene_classes_dicts_29 = {
    "building": ["apartment_building-outdoor", "building_facade", "office_building", "skyscraper"],
    "forest": ["bamboo_forest", "forest-broadleaf", "rainforest"],
    "snow_field": ["snowfield", "mountain_snowy"],
    "mountain": ["mountain"],
    "path": ["forest_path", "mountain_path"],
    "road": ["field_road", "forest_road", "desert_road"],
    "desert": ["desert-sand"],
    "football_field": ["football_field", "stadium-baseball", "stadium-football", "stadium-soccer"],
    "basketball_field": ["basketball_court-indoor"],
    "oldtown": ["oldtown"],
    "livingroom": ["living_room"],
    "kitchen": ["kitchen", "restaurant_kitchen", "galley"],
    "beach": ["beach"],
    "ocean": ["ocean"],
    "gym": ["gymnasium-indoor"],
    "water": ["river", "lake-natural", "moat-water"],
    "street": ["street", "crosswalk"],
    "picnic": ["picnic_area"],
    "park": ["park", "botanical_garden", "formal_garden", "japanese_garden", "topiary_garden"],
    "zen_garden": ["zen_garden"],
    "pagoda": ["pagoda"],
    "historic_building": ["palace", "ruin"],
    "grass_field": ["farm", "field-cultivated", "golf_course", "pasture"],
    "waterfall": ["waterfall"],
    "roadtrip": ["roadtrip"],
    "porch": ["porch"],
    "boardwalk": ["boardwalk"],
    "grotto": ["grotto"],
    "food": ["food"]
}

scene_classes_dicts_8 = {
    "natural": ["bamboo_forest", "forest-broadleaf", "rainforest", "forest_path", "mountain_path", "snowfield", "mountain_snowy", "mountain", "field_road", "river", "lake-natural",
                "farm", "field-cultivated", "golf_course", "pasture", "desert-sand", "waterfall", "skyline"],
    "park": ["park", "botanical_garden", "formal_garden", "japanese_garden", "topiary_garden", "parkgrass", "parkpicnic_1"],
    "beach_ocean": ["beach", "ocean"],
    "city": ["apartment_building-outdoor", "building_facade", "office_building", "skyscraper", "street", "crosswalk", "palace", "nightview"],
    "home_food": ["living_room", "kitchen", "galley", "food", "tablefood", "vegetablesfruits"],
    "sports_normal": ["football_field", "stadium-baseball", "stadium-football", "stadium-soccer"],
    "basketball_filed": ["basketball_court-indoor"],
    "gym": ["gymnasium-indoor"],
    "other": ["airplane_cabin", "auditorium", "fabric_store", "office", "amusement_arcade", "bus_interior", "gift_shop", "office_cubicles", "archive", "car_interior", "jewelry_shop", ],

    # "road": [, "forest_road", "desert_road"],
    # "oldtown": ["oldtown"],
    # "kitchen": [ "restaurant_kitchen", ],
    # "water": ["moat-water"],
    # "picnic": ["picnic_area"],
    # "zen_garden": ["zen_garden"],
    # "pagoda": ["pagoda"],
    # "historic_building": [, "ruin"],
    # "roadtrip": ["roadtrip"],
    # "porch": ["porch"],
    # "boardwalk": ["boardwalk"],
    # "grotto": ["grotto"],
}

scene_classes_dicts_10 = {
    "natural": ["bamboo_forest", "forest-broadleaf", "rainforest", "forest_path", "mountain_path", "snowfield", "mountain_snowy", "mountain", "field_road", "river", "lake-natural",
                "farm", "field-cultivated", "golf_course", "pasture", "desert-sand", "waterfall", "skyline", "scene_highway", "yellow_grass_sand"],
    "park": ["park", "botanical_garden", "formal_garden", "japanese_garden", "topiary_garden", "parkgrass", "parkpicnic_1"],
    "beach_ocean": ["beach", "ocean"],
    "city": ["apartment_building-outdoor", "building_facade", "office_building", "skyscraper", "street", "crosswalk", "palace", "nightview", "city_viaduct"],
    # "home_food": ["living_room", "kitchen", "galley", "food", "tablefood", "vegetablesfruits"],
    "home": ["living_room", "kitchen", "galley", "home"],
    "food": ["food", "tablefood", "vegetablesfruits", "food"],
    "sports_normal": ["football_field", "stadium-baseball", "stadium-football", "stadium-soccer"],
    "basketball_filed": ["basketball_court-indoor"],
    "gym": ["gymnasium-indoor"],
    "other": ["color_cornercase_0208", "airplane_cabin", "auditorium", "fabric_store", "office", "amusement_arcade",
              "bus_interior", "gift_shop", "office_cubicles", "archive", "car_interior", "jewelry_shop", "riding", "soil", "walk"
              "fmg_kidslide", "fmg_officedesktop", "fmg_parkinglot"
              ],

    # "road": [, "forest_road", "desert_road"],
    # "oldtown": ["oldtown"],
    # "kitchen": [ "restaurant_kitchen", ],
    # "water": ["moat-water"],
    # "picnic": ["picnic_area"],
    # "zen_garden": ["zen_garden"],
    # "pagoda": ["pagoda"],
    # "historic_building": [, "ruin"],
    # "roadtrip": ["roadtrip"],
    # "porch": ["porch"],
    # "boardwalk": ["boardwalk"],
    # "grotto": ["grotto"],
}

scene_classes_dicts_2_city = {
    "city": ["apartment_building-outdoor", "building_facade", "office_building", "skyscraper", "street", "crosswalk", "palace"],
    "other": ["airplane_cabin", "auditorium", "fabric_store", "office", "amusement_arcade", "bus_interior", "gift_shop", "office_cubicles", "archive", "car_interior", "jewelry_shop",
              "bamboo_forest", "forest-broadleaf", "rainforest", "forest_path", "mountain_path", "snowfield",
              "mountain_snowy", "mountain", "field_road", "river", "lake-natural",
              "farm", "field-cultivated", "golf_course", "pasture", "desert-sand", "waterfall",
              "park", "botanical_garden", "formal_garden", "japanese_garden", "topiary_garden",
              "beach", "ocean",
              "living_room", "kitchen", "galley", "food",
              "football_field", "stadium-baseball", "stadium-football", "stadium-soccer",
              "basketball_court-indoor",
              "gymnasium-indoor",
              ],
}

scene_names_list = ["building",
    "forest",
    "snow_field",
    "mountain",
    "path",
    "road",
    "desert",
    "football_field",
    "basketball_field",
    "oldtown",
    "livingroom",
    "kitchen",
    "beach",
    "ocean",
    "gym",
    "water",
    "street",
    "picnic",
    "park",
    "zen_garden",
    "pagoda",
    "historic_building",
    "grass_field",
    "waterfall",
    "roadtrip",
    "porch",
    "boardwalk",
    "grotto",
    "food"]

scene_names_list_10 = ["natural", "park", "beach_ocean", "city", "home", "food", "sports_normal", "basketball_filed", "gym", "other"]
scene_names_list_9 = ["natural", "park", "beach_ocean", "city", "home_food", "sports_normal", "basketball_filed", "gym", "other"]
scene_names_list_2_city = ["city", "other"]

def lookup_index(scene_name, scene_classes_dicts_):
    # print("there are " + str(len(scene_classes_dicts_)) + " classes finnally")
    # i = 0
    # for item in scene_classes_dicts_:
    #     print(item)
    #     print(scene_classes_dicts_[item])
    #     if scene_name in scene_classes_dicts_[item]:
    #         return i
    #     i = i + 1

    # i = 0
    for i, item in enumerate(scene_classes_dicts_):
        # print(item)
        # print(scene_classes_dicts_[item])
        if scene_name in scene_classes_dicts_[item]:
            return i
        # i = i + 1

# # sample test
# index = lookup_index("beach", scene_classes_dicts)
# print(index)


# dirs = os.listdir(root_dir)
# for dir in tqdm(dirs):
#     files = os.listdir(os.path.join(root_dir, dir))
#     for file in files:
#         train_txt.write(str(dir) + "/" + str(file) + " " + str(dir))
#         train_txt.write("\n")

remap_root = r"D:\datasets\fmg\cls_scene_fmg\other_val_remap_9"

dirs = os.listdir(root_dir)
for dir in tqdm(dirs):
    files = os.listdir(os.path.join(root_dir, dir))
    print("dir is ", dir)
    for file in tqdm(files):
        if file.endswith('.jpg'):
            # print(file)
            index = lookup_index(str(dir), scene_classes_dicts_10) # scene_classes_dicts_29  #   # scene_classes_dicts_9  # scene_classes_dicts_2_city
            if None == index:
                continue
            # print(index)
            # remap_root_dir = os.path.join(remap_root, scene_names_list_9[index]) #
            # if not os.path.exists(remap_root_dir):
            #     os.makedirs(remap_root_dir)
            # else:
            #     pass
            #     # print("dir path not exist: ", remap_root_dir)
            # shutil.copyfile(os.path.join(root_dir, dir, file), os.path.join(remap_root_dir, file))
            train_txt.write(str(dir) + "/" + str(file) + " " + str(index))
            train_txt.write("\n")
        else:
            continue