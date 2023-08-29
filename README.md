# Dell Optiplex BIOS Flash :zap:

Welcome to the definitive guide on modifying and fixing the BIOS of Dell Optiplex 7040/7050 MFF motherboards! Whether you're an experienced techie or just dipping your toes into BIOS tinkering, this document will walk you through the process step by step. And guess what? You're not alone on this journey. With the help of this guide and some assistance from ChatGPT, we'll have you mastering BIOS flashing in no time. 👨‍💻

## Overview

This comprehensive guide outlines the exact procedures for BIOS modification and replacement on Dell Optiplex 7040/7050 MFF motherboards. While the provided steps are applicable across Dell BIOS systems, please be mindful of potential variations in hex offset locations within the .bin file.
Hopefully these steps can help someone else out in the future.

**Update:** With some awesome help from ChatGPT, I now have a Python script that makes updating the Service Tag a breeze.

## Prerequisites

- **Working Motherboard**: Ensure the BIOS chip is operational. (Obviously this won't work if the chip is completely fried)
- **CH341A USB Programmer**: Get the [CH341A USB Programmer](https://www.amazon.com/KeeYees-SOIC8-EEPROM-CH341A-Programmer/dp/B07SHSL9X9/ref=sr_1_3?keywords=ch341a+programmer&qid=1693206571&sprefix=ch341A%2Caps%2C121&sr=8-3).
- **CH341A Flashing Software**: Download [CH341A Flashing Software](https://github.com/nofeletru/UsbAsp-flash/releases/).
    - Download the latest version of "**AsProgrammer_#.#.#.zip**"
- **HxD Hex Editor**: Download [HxD](https://mh-nexus.de/en/hxd/) for BIOS tinkering.
- **BIOS in BIN Format**: For replacement.
    - I've uploaded some known good files to this repository

## Backup Process (Step 1)

1. **Locate the BIOS Chip**: Find the 8-pin chip near the RAM slots surrounded by a white border.
    ![Dell BIOS chip with outline](https://jensd.be/wp-content/uploads/image-20.png)
    - Terrible image, but best example that I could find
2. **Record Chip Info**: Document the chip details for reference.
    - Example, my chip read "WINBOND 25Q128JVSQ"
3. **Configure Flashing Software**: Set up the flashing software and hardware.
    </br>
    ![Hardware menu dropdown](https://jensd.be/wp-content/uploads/image-17.png)
    - Easiest way to do this is to just click the icon with the green question mark, which should be able to detect your chips' type and settings. Make sure what you noted matches what was detected.
    - Otherwise, hover over "IC" then click "Search"
    - Leave out the brand, just type in the alphanumeric characters. You'll see the list shrink as it narrows down the available options. In my case, I had a WINBOND brand chip, so I used the option "W25Q128JV". You'll do the same for your particular brand.
4. **Assemble the Programmer**: Setup your programmer.
    - Grab the programmer, cable with clamp clip, and green pcb with one end configured for the cable and the other with 8 exposed pins
    - Look at the bottom side of your programmer, you should see an outline depicting how to align the green pcb depending on the chip being programmed.
    </br>
    ![CH341A Programmer](https://i5.walmartimages.com/asr/f8b2298c-f031-4da4-b9eb-44a83ecbc168.2688595ece2132b69c2c9668eac06f32.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF)
    - In our case, we will be using the "25 SPI BIOS" portion. So flip the board back upright, then insert the green pcb pins into the locking connector with pin 1 facing the locking lever and pin 8 in the holes closest to the USB connector. It should look similar to the image below.
    </br>
    ![Example of programmer correctly configured](https://i5.walmartimages.com/asr/9651009c-1d4a-496a-b29b-cd93b6d5cc0d.3f552d92e3b6142816e8728379d20ac0.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF)
    - Plug the USB into your computer
5. **Find the Chip**: Locate pin 1 on your BIOS chip
    - Look for a small round indent or a painted dot on the chip. The pin on the farthest edge closest to the indicator is pin 1.
    </br>
    ![Example BIOS chip pinout](https://scontent-lax3-1.xx.fbcdn.net/v/t1.6435-9/115912245_117879603339486_7850752308703871979_n.jpg?stp=dst-jpg_p526x296&_nc_cat=110&ccb=1-7&_nc_sid=8bfeb9&_nc_ohc=IeZof7P-yekAX-QyfEr&_nc_ht=scontent-lax3-1.xx&oh=00_AfApTtaoEeAbmKvlsO4mgL-OflyPnixDdhC1d4kdI_7Gng&oe=6513BEC8)
6. **Connect the Chip**: Connect the clamp clip to the BIOS chip
    - Look at the clip and find the red wire, this wire will be connected to pin 1 on the BIOS chip.
    - Pinch the clip to fully expand then place it onto the chip ensuring you've made good contact with all 8 pins
7. **Read the BIOS Chip**: Use the flashing software to read the chip.
    - Click the icon with the right pointing green arrow
    - The programmer will now begin reading the data stored on the chip. Wait for this process to complete. Should be 1-2 mins.
8. **Inspect and Save Data**: Verify the data and save it on your computer.
    - First, scroll through the data and ensure it looks like a jumbled mess of alphabetical characters and numbers. If you only see "FF" throughout, then you're probably not fully seated or aligned on to the chip.
    - If this is a brand new chip that was never flashed or simply erased, then ignore this and continue to the next step.
    - Click the save icon then title and save this file to memorable place on your computer.
9. **Repeat**: Re-run steps 9-11 once more
10. **Verify Data Integrity**: Open command prompt and navigate to the directory where the BIOS data was stored.
    - Run the following commands for both files:
    `certutil -hashfile <saved_bios>.bin md5`
    - Compare both hashes and ensure they're the same. If so, proceed. If not, stop because the data is corrupted.

## Modify/Replace Process (Step 2a/2b)

### 2a. Modify BIOS

#### Manual Way

1. **Open Hex Editor**: Launch HxD.
2. **Load Your BIOS File**: Click the Open file option and select the BIOS bin file that you want to modify.
    - In my case, I want to modify the Service Tag that was assigned to my motherboard. I've gone ahead and chosen my old BIOS that I backed up.
3. **Navigate the Hex Offset**: Locate the hex offset that you want to modify.
    - Again, in my case, I'm modifying the Service Tag info, so first I'll navigate to the Hex Offset.
    - Optiplex 7040/7050 Service Tags are saved in plain text at `78002A`. Scroll down until the left hand column shows `780020`.
4. **Find the Service Tag**: Identify the Service Tag location. Column `0A` is the start of the Service Tag. We know that Service Tags are always 7 characters, so the Tag is located in columns `0A-0F` and `780030 00`.
5. **Modify Safely**: Use "Search" > "Replace" to update the Service Tag.
    - Type in the existing Service Tag in the "Search For" then the desired Service Tag in the "Replace With". 
6. **Save Your Changes**: Save the modified BIOS file.
    - Continue on to the next section to upload your modified BIOS.

#### Scripted Method

1. **Python Script**: If you have python installed already, just double-click the Python script to run it. Otherwise, open command prompt and `cd` to the location of the file then run the script.
2. **Path Input**: Provide the file path. Either type in the absolute/relative path or drag 'n drop the bin file onto the terminal window then press <Enter>.
3. **Service Tag Update**: Choose to keep or replace the Service Tag.
4. **Confirmation**: Done! Your bin file has now been updated and you can continue to the next step.

### 2b. Replacing the BIOS

1. **Open the File**: Load your modified or new BIOS file.
2. **Step-by-Step**: Select the 4-step process from the dropdown menu.
    ![Programming Steps](https://jensd.be/wp-content/uploads/image-25.png)
3. **Confirmation**: Confirm the BIOS replacement.
4. **BIOS Replacement**: Let the program work its magic. This could take anywhere from 3-10 minutes.
    ![Status bar progress](https://jensd.be/wp-content/uploads/image-26.png)
5. **Finish Line**: Once this process completes, disconnect the programmer clip.
6. **Verification**: Test your newly flashed BIOS.

## References 🖇️
[BIOS or SPI programming on Windows or Linux using a CH341a MiniProgrammer](https://jensd.be/980/linux/bios-or-spi-programming-on-windows-or-linux-using-a-ch341a) by Jensd
  - Jensd does a way better job at explaining this than I do!
