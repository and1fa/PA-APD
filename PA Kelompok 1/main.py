import os
import json
from tabulate import tabulate

dataUser = 'data_user.json'
dataPasien = 'data_pasien.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def muatData(file):
    if not os.path.exists(file):
        return{}
    with open(file, 'r') as f:
        return json.load(f)
    
def simpanData(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def register():
    users = muatData(dataUser)
    while True: 
        username = input("Masukkan username : ")
        if not username:
            print ("Username tidak boleh kosong")
            continue
        if username in users:
            print ("Username sudah terdaftar")
            continue

        password = input("Masukkan password (maksimal 8 karakter) : ")
        if not password:
            print ("Password tidak boleh kosong")
            continue
        if len(password) > 8:
            print ("Password maksimal 8 karakter")
            continue

        users[username] = {'password' : password, 'role' : 'guest'}
        simpanData(dataUser, users)
        print ("Registrasi berhasil")
        break

def login():
    users = muatData(dataUser)
    kesempatan = 0
    while kesempatan < 3:
        username = input("Masukkan username : ")
        password = input("Masukkan password : ")

        if not username or not password:
            print ("Usernmae dan password tidak boleh kosong")
            kesempatan += 1
            continue
        if len(password) > 8:
            print ("Password maksimal 8 karakter")
            kesempatan += 1
            continue

        user = users.get(username)
        if user and user['password'] == password:
            print ("Login berhasil")
            return username, user['role']
        else:
            print ("Login gagal. Periksa username dan password")
            kesempatan += 1
    
    print ("Percobaan login habis")
    return None, None

def tambahDataPasien():
    pasien = muatData(dataPasien)
    idPasien = f"PSN{len(pasien) + 1:03}"

    try:
        nama = input("Nama pasien : ")
        umur = int(input("Umur pasien : "))
        jenisKelamin = input ("Jenis kelamin (L/P) : ")
        tinggi = float(input("Tinggi badan (cm) : "))
        berat = float(input("Berat badan (kg) : "))
        diagnosa = input("Diagnosa : ")
        ruangan = input("Ruangan pasien : ")
        dokter = input("Dokter yang bertanggung jawab : ")

        pasien[idPasien] = {
            "nama" : nama,
            "umur" : umur,
            "jenisKelamin" : jenisKelamin,
            "tinggi" : tinggi,
            "berat" : berat,
            "diagnosa" : diagnosa,
            "ruangan" : ruangan,
            "dokter" : dokter
        } 

        simpanData(dataPasien, pasien)
        print (f"Data pasien berhasil ditambahkan dengan ID {idPasien}")
    except ValueError as e:
        print ("Input tidak valid", e)

def lihatDataPasien(role):
    pasien = muatData(dataPasien)
    if not pasien:
        print ("Tidak ada pasien")
        return
    
    table = []
    headers = []
    for idPasien, pasien in pasien.items():
        if role == 'admin':
            table.append([
                idPasien, pasien['nama'],pasien['umur'], pasien['jenisKelamin'], 
                pasien['tinggi'], pasien['berat'], pasien['diagnosa'],
pasien['ruangan'], pasien['dokter']
            ])
            headers = ["ID Pasien", "Nama", "Umur", "Jenis Kelamin", "Tinggi(cm)",
"Berat(kg)", "Diagnosa", "Ruangan", "Dokter"]
            
        elif role == 'dokter':
            table.append([
                idPasien, pasien['nama'],pasien['umur'], pasien['jenisKelamin'], 
                pasien['tinggi'], pasien['berat'], pasien['diagnosa'],
pasien['ruangan'], pasien['dokter']
            ])
            headers = ["ID Pasien", "Nama", "Umur", "Jenis Kelamin", "Tinggi(cm)",
"Berat(kg)", "Diagnosa", "Ruangan", "Dokter"]
            
        elif role == 'ruangan':
            table.append([
                idPasien, pasien['nama'],pasien['umur'], pasien['jenisKelamin'], 
                pasien['tinggi'], pasien['berat'], pasien['diagnosa'],
pasien['ruangan'], pasien['dokter']
            ])
            headers = ["ID Pasien", "Nama", "Umur", "Jenis Kelamin", "Tinggi(cm)",
"Berat(kg)", "Diagnosa", "Ruangan", "Dokter"]
            
        elif role == 'guest':
            table.append([
                idPasien, pasien['nama'], pasien['ruangan']
            ])
            headers = ["ID Pasien", "Nama", "Ruangan"]
    
    print(tabulate(table, headers, tablefmt="heavy_grid"))

def ubahDataPasien():
    pasien = muatData(dataPasien)
    idPasien = input("Masukkan ID pasien yang ingin diperbarui : ")
    if idPasien in pasien:
        print ("Data saat ini : ", pasien[idPasien])
        pasien[idPasien]["diagnosa"] = input("Masukkan diagnosa baru : ")
        simpanData(dataPasien, pasien)
        print("Data pasien berhasil diperbarui")
    else:
        print ("ID pasien tidak ditemukan")

def hapusDataPasien():
    pasien = muatData(dataPasien)
    idPasien = input("Masukkan ID pasien yang ingin dihapus : ")
    if idPasien in pasien:
        del pasien[idPasien]
        simpanData(dataPasien, pasien)
        print ("Data pasien berhasil dihapus")
    else:
        print("ID pasien tidak ditemukan")

def menuAdmin():
    while True:
        print ("\n--- Menu Admin ---")
        print ("1. Lihat Data Pasien\n2.Tambah Data Pasien\n3. Ubah Data Pasien\n4. Hapus Data Pasien\n5. Logout")
        menuAdmin = input("Pilih menu : ")

        if menuAdmin == '1':
            lihatDataPasien("admin")
        elif menuAdmin == '2':
            tambahDataPasien()
        elif menuAdmin == '3':
            ubahDataPasien()
        elif menuAdmin == '4':
            hapusDataPasien()
        elif menuAdmin == '5':
            print ("Logout berhasil")
            break
        else:
            print ("Pilihan tidak valid")

def menuDokter():
    while True:
        print ("\n--- Menu Dokter ---")
        print ("1. Lihat Data Pasien\n2. Perbarui Diagnosa Pasien\n3. Logout")
        menuDokter = input("Pilih menu : ")

        if menuDokter == '1':
            lihatDataPasien("dokter")
        elif menuDokter == '2':
            ubahDataPasien()
        elif menuDokter == '3':
            print("Logout berhasil")
            break
        else:
            print ("Pilihan tidak valid")

def menuRuangan():
    while True:
        print ("\n--- Menu Ruangan ---")
        print ("1. Lihat Data Pasien di Ruangan\n2. Tambah Pasien\n3. Logout")
        menuRuangan = input("Pilih menu : ")

        if menuRuangan == '1':
            lihatDataPasien("ruangan")
        elif menuRuangan== '2':
            tambahDataPasien()
        elif menuRuangan == '3':
            print("Logout berhasil")
            break
        else:
            print ("Pilihan tidak valid")

def menuGuest():
    while True:
        print ("\n--- Menu Tamu ---")
        print ("1. Lihat Nama & Ruangan Pasien\n2. Logout")
        menuGuest = input("Pilih menu : ")

        if menuGuest == '1':
            lihatDataPasien("guest")
        elif menuGuest == '2':
            print ("Logout berhasil")
            break
        else:
            print ("Pilihan tidak valid")

def main():
    print ("Sistem Manajemen Pasien Rawat Inap Rumah Sakit")
    while True:
        print("\n1. Register\n2. Login\n3. Keluar")
        menu = input("Pilih menu : ")

        if menu == '1':
            register()
        elif menu == '2':
            username, role = login()
            if username:
                if role == 'admin':
                    menuAdmin()
                elif role == 'dokter':
                    menuDokter()
                elif role == 'ruangan':
                    menuRuangan()
                elif role == 'guest':
                    menuGuest()
                else:
                    print ("Login gagal")
        elif menu == '3':
            print ("Terimakasih")
            break
        else:
            print ("Pilihan tidak valid")

main()