import os


class KodYazici:
    def __init__(self):
        self.output_dir = "nexus_system/generated"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def calis(self, talimat):
        # Basit kod şablonları
        sifir = "print('Merhaba Dünya!')"
        hesap = "toplam = 5 + 3\nprint('Toplam:', toplam)"
        dongu = "for i in range(5):\n    print(f'Sayı: {i}')"

        if "merhaba" in talimat.lower():
            return self.dosyaya_yaz("hello.py", sifir)
        elif "hesap" in talimat.lower():
            return self.dosyaya_yaz("calculator.py", hesap)
        else:
            return self.dosyaya_yaz("program.py", dongu)

    def dosyaya_yaz(self, dosya_adi, kod):
        file_path = os.path.join(self.output_dir, dosya_adi)
        with open(file_path, "w") as f:
            f.write(kod)
        return f"{file_path} oluşturuldu"
