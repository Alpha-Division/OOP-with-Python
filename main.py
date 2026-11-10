class karakter():
    def __init__(self, nama, level, hp, role, maxhp):
        self.maxhp = maxhp
        self.nama = nama
        self.level = level
        self.hp = hp
        self.role = role

    def serang(self, target):
        damage = int(input("Damage : "))

        if target.hp <= 0:
            target.hp = 0
            print(f"{target.nama} sudah mati, tidak bisa diserang")
        elif target.hp > 0:
            target.hp = max(0, target.hp - damage) 
            print(f"{target.nama} diserang oleh {self.nama}, hp berkurang menjadi {target.hp}")

            if target.hp == 0:
                print(f"{target.nama} telah dikalahkan!")

    def heal(self, target):
        output = int(input("Heal : "))

        if target.hp <= 0:
            target.hp = 0
            print(f"{target.nama} sudah mati, tidak bisa melakukan heal")

        elif target.hp < target.maxhp:
            target.hp = min(target.maxhp, target.hp + output)
            print(f"Heal berhasil! HP bertambah menjadi : {target.hp}")

        else:
            print(f"{target.nama} memiliki HP maksimum!")

    def tampilkan_info(self):
        print(f"\nNama: {self.nama}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}")
        print(f"Role: {self.role}")

def make_char():
    nama = input("Buat nama : ")
    level = 1
    hp = 100
    maxhp = 100

    print("1.Assasin")
    print("2.Tank")
    print("3.Mage")
    print("4.Fighter")

    role = input("Choose your role : ")

    karakter1 = karakter(nama, level, hp, role, maxhp)

    return karakter1

karakter1 = make_char()
karakter2 = karakter("Julian", 5, 120, "Archer", 130)

def move():
    print("1.Attack")
    print("2.Heal")
    print("3.Defense")

    moveset = input("Choose your move : ")

    if moveset == "1":
        karakter1.serang(karakter2)
    elif moveset == "2":
        karakter1.heal(karakter2)

# karakter1.serang(karakter2)
# karakter1.heal(karakter2)

move()

karakter1.tampilkan_info()
karakter2.tampilkan_info()
