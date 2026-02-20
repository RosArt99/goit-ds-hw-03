from pymongo import MongoClient
from pymongo.server_api import ServerApi
from create_DB import get_client, insert_initial_data

db = get_client().book #DB connecting and path

insert_initial_data(db)

#----------------------FUNCTIONS-------------------------------------------

def get_all_docs(db): #getting data, but not showing yet
    return list(db.cats.find({}))

def show_all_docs(db): #showing data with separated style
    for el in get_all_docs(db):
        print("-" * 50)
        for k, v in el.items():
            print(f"{k}: {v}")

def get_info_by_name(db, name): #same, getting only
        return db.cats.find({'name': {'$eq': name}})

def show_info_by_name(db, name): #showing
        try:
            result = list(get_info_by_name(db, name))

            if not result:
                print("No doc found")
                return

            for el in result:
                print("-" * 50)
                for k, v in el.items():
                    print(f"{k}: {v}")

        except Exception as e:
            print("Unknown error: ", e)

def update_age_by_name(db, name, new_age):
    result = db.cats.update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )
    if result.matched_count == 0:
        print(f"No user found with name: {name}")
    elif result.modified_count == 0:
        print("Same age entered")
    else:
        print("Age updated")

def add_new_feature(db, name, feature):
    result = db.cats.update_one(
        {"name": name},
        {"$addToSet": {"features": feature}}
    )

    if result.matched_count == 0:
        print("User not found")
    elif result.modified_count == 0:
        print("Entered feature exists")
    else:
        print("Feature added")

def delete_by_name(db, name):
    result = db.cats.delete_one({"name": name})

    if result.deleted_count == 0:
        print(f"No user found with name: {name}")
    else:
        print(f"{name} was deleted")

def delete_all(db):
    result = db.cats.delete_many({})
    print(f"Deleted {result.deleted_count} documents from the collection.")

#-------------------------MAIN----------------------------------------

if __name__ == '__main__':
    show_all_docs(db) #виведення всіх записів із колекції.

    name = input("Enter name: ")
    show_info_by_name(db, name) #ввести ім'я та виводить інформацію про цього.
    
    name_update_age = input("Enter name to update age: ") #оновити вік за ім'ям.
    try:
        new_age = int(input(f"Enter new age for {name_update_age}: "))
        update_age_by_name(db, name_update_age, new_age)
    except ValueError:
        print("Invalid age. Must be a number.")

    name_feature = input("Enter name to add feature: ")
    feature = input(f"Enter new feature to add for {name_feature}: ") #додати нову характеристику до списку features кота за ім'ям.
    add_new_feature(db, name_feature, feature)
    #видалення запису з колекції за ім'ям
    name_delete = input("Enter name to delete: ")  

while True: #recurring cycle
    delete_confirm = input(f"Do you want to delete {name_delete}? (y/n): ").strip().lower() # видалення запису за ім'ям
    
    if delete_confirm == 'y':
        delete_by_name(db, name_delete)
        break
    elif delete_confirm == 'n':
        print("Deletion cancelled.")
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.") #invalid input solving


while True: #recurring cycle
    confirm_delete_all = input("Do you want to delete ALL documents? (y/n): ").strip().lower()# видалення документів
    
    if confirm_delete_all == 'y':
        delete_all(db)
        break
    elif confirm_delete_all == 'n':
        print("Deletion of all documents cancelled.")
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.") #invalid input solving