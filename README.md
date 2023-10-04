**USBRaspberyPIAttack**


**Purpose:**
1. It can retrive Files, Information from the target PC, by plugging couple of USB device.
2. Can be used to invoke programs in the target PC where its plugged.
3. Pull up the Wifi Information of the Host device and connect to it.

**Things Required**
1. Two SBC boards with wifi and gadget mode compatitbility, Rapsbery PI Zero W and PI Zero 2 W used in this project.

**How it Works**
1. Both Pi1 and Pi2 has to be plugged into the Host PC.
2. Once the HOST PC is powered on Both Pi1 and Pi2 will boot up along with Host PC.
3. Pi1 will act as an Access point.
4. Pi2 will wait for the Pi1, once its available, it gets connected to Pi1.
5. Pi1 will attach emulated USB to HOST PC (which has the program to be executed in the host) and will wait until the Host PC is fully operational.
6. Once the Host PC is operational Pi1 will send attack singal to Pi2.
7. Pi2 acts as Keyboard, using the Sendkeys it will execute the program which is located in the attached USB.

**Note:**
1. We can attach the Pi to already turned on machine as well, it will work.
2. It will start attack only when Host PC to be operational, so the chance of sucess is 100%.
3. As we have the USB attached to Host PC we can write any kind of program to attcak, no limitation.

**Instructions**
1. Image file for both PiZeroW and PiZero2W attached in the release.
2. If you want to use you own Attack program , update the files pExFatUSB drive.

**More about the Image**
1. Both Pi1 and Pi2 runs on Embeded custom Linux OS
2. used custom OS so that the device gets ready at rapid phase

![image](https://github.com/PaulJenkin/UsbPiAttack/assets/47582098/aefd618c-1a58-400b-9ecb-0edfe2f2bbf7)
