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
            target.hp = target.hp - damage
            print(f"{target.nama} diserang oleh {self.nama}, hp berkurang menjadi {target.hp}")
        else:
            target.hp = target.hp - damage
            print(f"{target.nama} mati, HP tersisa {target.hp}")

    def heal(self, target):
        output = int(input("Heal : "))
        total = 0
        if target.hp <= 0:
            target.hp = 0
            print(f"{target.nama} sudah mati, tidak bisa melakukan heal")
        elif target.hp < target.maxhp:
            if target.hp + output > target.maxhp:
                total = target.hp - target.maxhp
                target.hp = target.hp - total 
            else:
                target.hp = target.hp + output
            print(f"Heal berhasil! HP bertambah menjadi : {target.hp}")

    def tampilkan_info(self):
        print(f"\nNama: {self.nama}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}")
        print(f"Role: {self.role}")

karakter1 = karakter("Martin", 11, 150, "Tank", 200)
karakter2 = karakter("Julian", 5, 120, "Archer", 130)

karakter1.serang(karakter2)
karakter1.heal(karakter2)

karakter1.tampilkan_info()
karakter2.tampilkan_info()
