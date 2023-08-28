# Dell Optiplex BIOS Flash

This is a short document to record the steps I took to modify/fix the bios of several Optiplex 7040/7050 MFF motherboards. These steps _should_ apply to all Dell BIOS, but the hex offset location in the .bin file may be different.

Hopefully these steps can help someone else out in the future.

## Requirements
- Motherboard with working BIOS chip (obviously this won't work if the chip is completely fried)
- [CH341A USB Programmer](https://www.amazon.com/KeeYees-SOIC8-EEPROM-CH341A-Programmer/dp/B07SHSL9X9/ref=sr_1_3?keywords=ch341a+programmer&qid=1693206571&sprefix=ch341A%2Caps%2C121&sr=8-3)
    - This is the exact one that I used. **Be aware** this model doesn't come with a switching voltage regulator, so this only works on chips with a 5V requirement. For our use case, this programmer will work just fine for majority of Motherboard/HDD BIOS chips, but will need to be physically modified for 1.8V/3.3V chips.
- [CH341A Flashing Software](https://github.com/nofeletru/UsbAsp-flash/releases/)
    - Download the latest version of "**AsProgrammer_#.#.#.zip**"
- [HxD](https://mh-nexus.de/en/hxd/) - Hex Editor
    - Download this software if modifying your BIOS
- New BIOS in BIN format (if replacing your own)
    - I've uploaded some known good files to this repository

## Backup Process (Step 1)
1. Locate the BIOS chip on your motherboard
    - Look for an 8-pin chip near the RAM slots surrounded by a white border.
    ![Dell BIOS chip with outline](https://jensd.be/wp-content/uploads/image-20.png)
    - Terrible image, but best example that I could find
2. Make note of what is written on your BIOS chip
    - This is one of the hardest parts, if you don't have a microscope or eagle vision. Luckily, I was able to use my phones' camera and flashlight to find mine, but it's not easy when your phone won't focus. :roll_eyes:
    - For example, my chip read "WINBOND 25Q128JVSQ"
3. Open the flashing software and configure your Hardware
    ![Hardware menu dropdown](https://jensd.be/wp-content/uploads/image-17.png)
4. Configure the software for your particular chip
    - Easiest way to do this is to just click the icon with the green question mark, which should be able to detect your chips' type and settings. Make sure what you noted matches what was detected.
    - Otherwise, hover over "IC" then click "Search"
    - Leave out the brand, just type in the alphanumeric characters. You'll see the list shrink as it narrows down the available options. In my case, I had a WINBOND brand chip, so I used the option "W25Q128JV". You'll do the same for your particular brand.
5. Once configured, setup your programmer
    - Grab the programmer, cable with clamp clip, and green pcb with one end configured for the cable and the other with 8 exposed pins
    - Look at the bottom side of your programmer, you should see an outline depicting how to align the green pcb depending on the chip being programmed.
    ![CH341A Programmer](https://i5.walmartimages.com/asr/f8b2298c-f031-4da4-b9eb-44a83ecbc168.2688595ece2132b69c2c9668eac06f32.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF)
    - In our case, we will be using the "25 SPI BIOS" portion. So flip the board back upright, then insert the green pcb pins into the locking connector with pin 1 facing the locking lever and pin 8 in the holes closest to the USB connector. It should look similar to the image below.
    ![Example of programmer correctly configured](https://i5.walmartimages.com/asr/9651009c-1d4a-496a-b29b-cd93b6d5cc0d.3f552d92e3b6142816e8728379d20ac0.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF)
6. Plug the USB into your computer
7. Locate pin 1 on your BIOS chip
    - Look for a small round indent or a painted dot on the chip. The pin on the farthest edge closest to the indicator is pin 1.
    ![Example BIOS chip pinout](https://scontent-lax3-1.xx.fbcdn.net/v/t1.6435-9/115912245_117879603339486_7850752308703871979_n.jpg?stp=dst-jpg_p526x296&_nc_cat=110&ccb=1-7&_nc_sid=8bfeb9&_nc_ohc=IeZof7P-yekAX-QyfEr&_nc_ht=scontent-lax3-1.xx&oh=00_AfApTtaoEeAbmKvlsO4mgL-OflyPnixDdhC1d4kdI_7Gng&oe=6513BEC8)
8. Connect the clamp clip to the BIOS chip
    - Look at the clip and find the red wire, this wire will be connected to pin 1 on the BIOS chip.
    - Pinch the clip to fully expand then place it onto the chip ensuring you've made good contact with all 8 pins
9. In the flashing software, read the BIOS chip
    - Click the icon with the right pointing green arrow
    - The programmer will now begin reading the data stored on the chip. Wait for this process to complete. Should be 1-2 mins.
10. Once the process is complete, inspect the data.
    - First, scroll through the data and ensure it looks like a jumbled mess of alphabetical characters and numbers. If you only see "FF" throughout, then you're probably not fully seated or aligned on to the chip.
    - If this is a brand new chip that was never flashed or simply erased, then ignore this and continue to the next step.
11. Save the data
    - Click the save icon then title and save this file to memorable place on your computer.
12. Re-run steps 9-11 once more
13. Open command prompt and navigate to the directory where the BIOS data was stored.
    - Run the following commands for both files:
    `certutil -hashfile <saved_bios>.bin md5`
    - Compare both hashes and ensure they're the same. If so, proceed. If not, stop because the data is corrupted.

## Modify/Replace Process (Step 2a/2b)

### 2a. Modify BIOS
1. Open the Hex Editor software, HxD
2. Click the Open file option and select the BIOS bin file that you want to modify.
    - In my case, I want to modify the Service Tag that was assigned to my motherboard. I've gone ahead and chosen my old BIOS that I backed up.
3. From here, you'll either need to know what you're looking for or what it is you want to modify. Again, in my case, I'm modifying the Service Tag info, so first I'll navigate to the Hex Offset.
4. Optiplex 7040/7050 Service Tags are saved in plain text at `78002A`. Scroll down until the left hand column shows `780020`.
5. Column `0A` is the start of the Service Tag. We know that Service Tags are always 7 characters, so the Tag is located in columns `0A-0F` and `780030 00`.
6. To modify this selection, I just use the replace method as I find it the safest.
    - Click "Search" then "Replace". Type in the existing Service Tag in the "Search For" then the desired Service Tag in the "Replace With". 
7. After the change has been made, Click "File" then "Save As".
8. Continue on to the next section to upload your modified BIOS.

### 2b. Replace BIOS
1. Click "Open file" then choose either the modified BIOS or the new one
2. To the right of the left facing red arrow icon is a drop down menu. Click that dropdown menu and click on the 4 step process.
    ![Programming Steps](https://jensd.be/wp-content/uploads/image-25.png)
3. Choose "Yes"
4. Let the program work its magic. This could take anywhere from 3-10 minutes.
    ![Status bar progress](https://jensd.be/wp-content/uploads/image-26.png)
5. Once this process completes, disconnect the programmer clip from the BIOS chip.
6. Feel free to test out your newly flashed motherboard.

## References 🖇️
[BIOS or SPI programming on Windows or Linux using a CH341a MiniProgrammer](https://jensd.be/980/linux/bios-or-spi-programming-on-windows-or-linux-using-a-ch341a) by Jensd
  - Jensd does a way better job at explaining this than I do!
