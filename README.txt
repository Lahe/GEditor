#README
1. Python algfailid asuvad kaustas python_kood
2. Programmi repositoorium: https://github.com/SpreeHD/GEditor

##
1. Python files are in the python_kood folder
2. Github repo: https://github.com/SpreeHD/GEditor

#Kasutusjuhend / Instruction manual

1. Avage fail GEditor.exe.
2. Otsige üles videofail, mida soovite muuta.
3. Valige kaust, kuhu soovite faili salvestada.
4. Valige funktsioon, sisestage väärtused ning vajutage käivitamisnupule.
5. Uus fail ilmub valitud kausta.

1. Open GEditor.exe.
2. Select the input path to your video file.
3. Choose an output path.
4. Choose a function, enter your desired values and click on the respective button to execute the function.
5. A new file will be created in your chosen output path.

#Available functions:
1.) Choose LUT: Changes the colors of a video file. Download a LUT (Lookup table) *.cube file and apply it to your video.
2.) Change Codec: Changes the codec of a video file. Works on almost all other functions, pressing "Change Codec" is not necessary.
3.) Change Speed: Changes the speed of a video file.
4.) Extract Subclip: Extracts a clip with the desired length from a video.
5.) Crop Video: Crops the height and width of a video by the desired amount of pixels.
6.) Convert to MP3: Converts a video file to a audio-only *.mp3 file.
7.) Save as GIF: Saves a video as *.gif.
8.) Stabilize Video: Stabilizes a video. (Warning: takes a while)
9.) Upload to Streamable/Gfycat: Uploads a video file to either Streamable or Gfycat. Link appears in the console.
10.) Custom Commands: You're able to execute custom ffmpeg commands with GEditor.
Enter a command you would execute with ffmpeg normally. Errors are shown in console. Example: "-i input.mp4 output.webm"