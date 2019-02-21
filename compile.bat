pyinstaller -F -w -i "C:\Users\chris\OneDrive\MeineDokumente\Schule\Itech\AE\PythonSkripte\Screen2OCR\logo.ico" "C:\Users\chris\OneDrive\MeineDokumente\Schule\Itech\AE\PythonSkripte\Screen2OCR\Screen2OCR.py"
pause
robocopy /Move "C:\Windows\System32\dist" "C:\Users\chris\OneDrive\MeineDokumente\Schule\Itech\AE\PythonSkripte\Screen2OCR"
robocopy /Move "C:\Windows\System32\build" "C:\Users\chris\OneDrive\MeineDokumente\Schule\Itech\AE\PythonSkripte\Screen2OCR"
robocopy /Move "C:\Users\chris\OneDrive\MeineDokumente\Schule\Itech\AE\PythonSkripte\Screen2OCR\dist\Screen2OCR.exe" "C:\Users\chris\OneDrive\MeineDokumente\Schule\Itech\AE\PythonSkripte\Screen2OCR\"
robocopy /MIR "C:\Windows\System32\dist"
pause