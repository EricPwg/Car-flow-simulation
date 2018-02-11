電腦環境需求
Python3.6(Anaconda)
Matplotlib
Windows較佳

各檔案使用說明:
00setting_tk.py
1. "light"可以設定紅綠燈參數:產生檔案 *_light.set.txt
2. "car"可以設定車輛參數:產生檔案 *_car.set.txt
3. "main"可以設定道路的基本參數:產生檔案 *_main.set.txt
4. "create folder"可以大量產生資料夾

01test_tk.py
批次執行模擬程式

02plot_figure_tk.py
批次執行將模擬結果畫圖

03plot_figure.py
個別專案畫圖，若需要動畫要用這個畫

使用方法:
1.用00setting_tk.py設定單一道路的基本參數，並產生3種設定檔
2.新增一個資料夾，將三種設定檔各放一個在裡面，稱該資料夾為專案(test3為設置好的範例專案)
3.用01test_tk.py選擇欲模擬專案專案，開始批次模擬，會產生一些模擬結果
4.用02plot_figure_tk.py選擇欲畫圖的專案，開始批次畫圖
5.若想畫動畫可以用03plot_figure.py，記得在檔案開頭對應處輸入正確的模擬id