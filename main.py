import pickle
import os


def DisplayMenu() -> None:
    print("1. Kayıtları Listele")
    print("2. Kayıt Ara")
    print("3. Kayıt Ekle")
    print("4. Kayıt Sil")
    print("5. Çıkış")
    print()


def MenuLoop() -> str:
    while True:
        DisplayMenu()
        option = input("Seçenek (1-5): ")
        print("\n")
        if option.isdigit() and 1 <= int(option) <= 5:
            break
    return option


def MainLoop() -> None:
    while True:
        option = MenuLoop()
        if option == "1":
            ListRecords()
        elif option == "2":
            SearchRecord()
        elif option == "3":
            AddRecord()
        elif option == "4":
            DeleteRecord()
        elif option == "5":
            break


def ListRecords() -> None:
    recordsList = ReadFile()
    print(f"Kayıt Sayısı: {len(recordsList)}\n")
    print(f"{'İsim':^10} {'Soyisim':^10} {'Telefon':^11}")
    for record in recordsList:
        print(
            f"{record.get('name', ' '):10.10} {record.get('surName', ' '):10.10} {record.get('telNumber', ' '):11.11}")
    print()


def SearchRecord() -> None:
    print("Kayıt Arama")
    name = input("İsim: ")
    surName = input("Soyisim: ")
    recordsList = SearchRecordFromFile(name, surName)
    print("Telefon Numarası: ", end='')
    for record in recordsList:
        print(f"{record.get('telNumber'):11.11}", end='')
    print("\n")



def AddRecord() -> None:
    print("Yeni Kayıt Ekle")
    name = input("İsim: ")
    surName = input("Soyisim: ")
    telNumber = input("Telefon Numarası: ")
    print(f"Yeni kayıt: {name} {surName} - {telNumber}")
    if AreYouSure():
        AddRecordToFile(name, surName, telNumber)
        print("Kayıt Eklendi\n")


def DeleteRecord() -> None:
    print("Kayıt Silmek")
    name = input("İsim: ")
    surName = input("Soyisim: ")
    recordsList = SearchRecordFromFile(name, surName)
    print("Telefon Numarası: ", end='')
    for record in recordsList:
        print(f"{record.get('telNumber'):11.11}", end='')
    print("\n")
    if AreYouSure():
        DeleteRecordsFromFile(recordsList)
        print("Kayıt Silindi\n")


def AreYouSure() -> bool:
    while True:
        answer = input("Eminmisiniz? (E)vet/(H)ayır")
        print()
        if answer.upper() == "E":
            return True
        elif answer.upper() == "H":
            return False


def ReadFile() -> list:
    try:
        with open("data.bin", "rb") as fileObject:
            recordsList = pickle.load(fileObject)
    except FileNotFoundError:
        recordsList = list()
    except Exception:
        print("Dosya diskten okunurken hata oluştu.")
        recordsList = list()

    return recordsList


def WriteFile(recordsListParam: list) -> None:
    try:
        with open("data.bin", "wb") as fileObject:
            pickle.dump(recordsListParam, fileObject)
    except Exception:
        print("Dosya yazılırken diskte bir hata oluştu.")


def SearchRecordFromFile(nameParam: str, surNameParam: str) -> list:
    recordsList = ReadFile()
    responseList = list()
    for record in recordsList:
        if record.get("name").upper() == nameParam.upper() and \
                record.get("surName").upper() == surNameParam.upper():
            responseList.append(record)
    return responseList


def AddRecordToFile(nameParam: str, surNameParam: str, telNumberParam: str) -> None:
    recordsList = ReadFile()
    recordDict = dict(name=nameParam, surName=surNameParam, telNumber=telNumberParam)
    recordsList.append(recordDict)
    WriteFile(recordsList)


def DeleteRecordsFromFile(recordsListParam : list) -> None:
    recordsList = ReadFile()
    for record in recordsList:
        for recordForDelete in recordsListParam:
            if record.get("name") == recordForDelete.get("name") and \
                record.get("surName") == recordForDelete.get("surName"):
                recordsList.remove(recordForDelete)
                continue
    WriteFile(recordsList)

MainLoop()
