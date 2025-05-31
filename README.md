# MikuMikuDB エディター

> Project Diva 向けの `mod_pv_db.txt` ファイルを生成するための GUI アプリケーション。  
> 日本語版 `MikuMikuDB エディター.exe` を提供します。（Python 3.12 で開発。配布ファイルは `.exe` のみで、元の `.py` ファイルは含まれていません。）

---

## 目次

1. [概要](#概要)  
2. [機能一覧](#機能一覧)  
3. [必要要件](#必要要件)  
4. [インストール](#インストール)  
5. [使い方](#使い方)  
6. [設定 & 自動保存](#設定--自動保存)  
7. [`mod_pv_db.txt` の生成](#mod_pv_dbtxt-の生成)  
8. [ファイル構成](#ファイル構成)  
9. [ライセンス](#ライセンス)  
10. [謝辞](#謝辞)  

---

## 概要

本アプリケーションは、Project Diva の楽曲パック向けに必要な `mod_pv_db.txt` を簡単に生成できる GUI ツールです。  
- **日本語版（MikuMikuDB エディター）**：すべてのラベル・メニュー・ダイアログが日本語表示。  
- **開発環境:** Python 3.12  
- **配布形式:** Windows 向けの `.exe` 実行ファイルのみを含む（元の `.py` スクリプトは同梱されていません）。  

ダウンロードした `.exe` を実行するだけで、すぐに GUI が立ち上がり操作できます。

---

## 機能一覧

- **日本語インターフェース**  
  - すべてのラベル、メニュー、ダイアログが日本語表示  
- **楽曲パック情報設定**  
  - 「Song Pack Name (英文字)」にパック名（ローマ字）を入力  
  - 「Japanese name (日本語)」に日本語のパック名を入力（任意）  
- **複数楽曲対応**  
  - 楽曲リストをツリービューで一覧表示（PV ID、オリジナル名、英語名）  
  - 「楽曲追加」「楽曲編集」「楽曲削除」ボタンで自由に楽曲を管理  
- **楽曲設定項目**  
  1. **PV ID**（例: `1131`）  
  2. **楽曲タイトル**:  
     - オリジナル名  
     - 英語名  
     - 代替英語名（任意）  
     - ひらがな名  
     - ローマ字名  
  3. **技術情報**:  
     - **BPM**  
     - **Date (YYYYMMDD)**  
     - **Sabi start time**（サビ開始時間）  
     - **Sabi duration**（サビの長さ）  
  4. **難易度設定**（「Difficulties」タブ）:  
     - **Easy** / **Normal** / **Hard** / **Extreme** / **Extra Extreme** の各チェックボックス  
     - チェックを入れると「Level」欄に任意の PV_LV_XXX を入力可能  
  5. **出演者**（「Performers」タブ）:  
     - リストボックスで追加済みの出演者を確認  
     - 「Add」ボタンでプルダウンから選択肢（MIK, RIN, LEN, LUK, KAI, MEI, HAK, NER, SAK, TET）を追加  
     - 「Remove」ボタンで選択中の出演者を削除  
  6. **楽曲情報**（「Song Information」タブ）:  
     - **Original** セクションに編曲者 / ギタープレイヤー / 作詞者 / マニピュレーター / Composer/Artist / PV Editor を入力（任意）  
     - **English** セクションに英語版同項目（Arranger (EN) / Guitar Player (EN) / Lyricist (EN) / Manipulator (EN) / Composer/Artist (EN) / PV Editor (EN)）を入力（任意）  
  7. **オーディオバリアント**（「Audio Variants」タブ）:  
     - 「Add Variant」で「Configure Audio Variant」ダイアログを表示  
       - **Variant name:**（バリアント名）  
       - **English name:**（英語名）  
       - **Alternative English name:**（代替英語名）  
       - **Romanized name:**（ローマ字名）  
       - **Variant artist:**（アーティスト）  
       - **Artist in English:**（アーティスト英語名）  
       - 「Accept」で入力を保存／「Cancel」でキャンセル  
     - 「Edit Variant」で選択中のバリアントを編集  
     - 「Remove Variant」で選択中のバリアントを削除  
     - バリアント一覧はツリービューに「Original Name」「English Name」「Artist」列で表示  
- **自動保存**  
  - 5 分ごとに現在の設定を `Autosaves/` フォルダに `.pdpack` として自動保存  
  - 最大 60 件まで保存し、それを超えると古いものから削除  
- **設定の保存・読込**  
  - メイン画面の「Save Configuration」ボタンで手動保存（拡張子 `.pdpack`、JSON形式）  
  - 「Load Configuration」ボタンで任意の `.pdpack` を読み込み、前回の状態を復元  
  - 「Load Autosave」ボタンで自動保存ファイル一覧を表示し、復元可能  
- **`mod_pv_db.txt` の生成**  
  - メイン画面の「Generate File」ボタンをクリックすると保存先ダイアログが表示  
  - ファイル名（デフォルト `mod_pv_db.txt`）と保存先を指定すると、UTF-8 形式で出力される  

---

## 必要要件

- **Windows 10/11**（`.exe` を実行できる環境）  
- Python 3.12 は開発用のみ。エンドユーザーは `.exe` のみ実行すれば OK。  

---

## インストール

1. GitHub リポジトリの「Releases」ページにアクセス。  
2. 日本語版実行ファイル **`MikuMikuDB エディター.exe`** をダウンロード。  
3. ダウンロードした `.exe` をダブルクリックして実行。  
   - Windows によってはセキュリティ警告が表示される場合があります。  
   - その場合は右クリック → 「プロパティ」 → 「ブロックの解除」にチェック → 「適用」をしてから再度実行してください。  

---

## 使い方

1. **`MikuMikuDB エディター.exe`** を実行して起動。  
2. メインウィンドウが開くと、上部に **「MikuMikuDB エディター」** と表示されます。  
3. **楽曲パック情報** を入力:  
   - 「Song Pack Name (英文字)」にパック名をローマ字で入力  
   - 必要であれば「Japanese name (日本語)」に日本語名を入力  
4. **楽曲リスト操作**:  
   - 「楽曲追加」ボタンをクリック → 「Configure Song」ダイアログを開く  
     - **Basic Information** タブで PV ID, Original name, English name, Alternative English name, Hiragana name, Romanized name, BPM, Date, Sabi start time, Sabi duration を入力  
     - **Difficulties** タブで「Easy」「Normal」「Hard」「Extreme」「Extra Extreme」にチェックを入れ、各「Level」欄に `PV_LV_XXX` を入力  
     - **Performers** タブで「Select character」プルダウンからキャラクターを選択 → 「Add」ボタンでリストに追加  
     - **Song Information** タブで編曲者 / ギタープレイヤー / 作詞者 / マニピュレーター / Composer/Artist / PV Editor をコピー＆ペースト  
     - **Audio Variants** タブで「Add Variant」をクリック → 「Configure Audio Variant」ダイアログ  
       - 必要項目を入力（Variant name, English name, Alternative English name, Romanized name, Variant artist, Artist in English） → 「Accept」で保存  
       - バリアントがリストに追加される  
     - 入力が完了したらダイアログの **「Accept」** ボタンをクリックして楽曲をリストに登録  
   - 楽曲をリストから選択して「楽曲編集」ボタンで再編集、「楽曲削除」ボタンでリストから削除  
5. すべての楽曲を追加・編集したら、メインウィンドウ右下の **「Generate File」** ボタンをクリック  
   - 保存ダイアログが開くので、ファイル名（例: `mod_pv_db.txt`）と保存先を指定して「保存」  
   - UTF-8 形式の `mod_pv_db.txt` が生成される  
6. 生成された `mod_pv_db.txt` を Project Diva のカスタム楽曲パックに組み込んで利用  

---

## 設定 & 自動保存

- **Auto-Save:**  
  - 5 分ごとに現在の設定を `Autosaves/` フォルダに `.pdpack` として自動保存  
  - 最新 60 件まで保存し、超過すると最も古いファイルから削除  
- **Save Configuration:**  
  - メイン画面の「Save Configuration」ボタンをクリック  
  - 任意の場所に `.pdpack` ファイルを保存（JSON形式・拡張子 `.pdpack`）  
- **Load Configuration:**  
  - メイン画面の「Load Configuration」ボタンをクリック  
  - 任意の `.pdpack` ファイルを選択して読み込み、パック名・楽曲リスト・設定を復元  
- **Load Autosave:**  
  - メイン画面の「Load Autosave」ボタンをクリック  
  - `Autosaves/` フォルダ内の最新の自動保存ファイル一覧を表示 → 選択 → 読み込み  

---

## `mod_pv_db.txt` の生成

1. 事前に以下を確認:  
   - **Song Pack Name** が入力されている  
   - **少なくとも 1 曲** がリストに登録されている  
2. メイン画面の **「Generate File」** をクリック  
3. 保存ダイアログでファイル名（デフォルト: `mod_pv_db.txt`）と保存先を指定し、「保存」をクリック  
4. 正しく出力されると「成功」メッセージが表示され、UTF-8 形式の `mod_pv_db.txt` が生成される  
5. 出力されたファイルを Project Diva のカスタムパックにそのまま組み込んで使用可能  

---

## ファイル構成

```

├── LICENSE                          # MIT License
├── README.md                        # この README ファイル
├── MikuMikuDB エディター.exe        # 日本語版実行ファイル
└── Autosaves/                       # 自動保存 (.pdpack) が格納されるフォルダ

```

- **`MikuMikuDB エディター.exe`**: 日本語版の実行ファイル  
- **`Autosaves/`**: 起動後に自動生成されるフォルダ。定期的に `.pdpack` ファイルが保存される  

---

## ライセンス

このプロジェクトは **MIT License** の下で公開されています。詳細は [LICENSE](./LICENSE) ファイルをご参照ください。

---

## 謝辞

- Project Diva モッディングコミュニティの皆さまに感謝します。  
- 開発: **NyxC**  
- 特別な感謝: ベータテスターおよびフィードバックをくださった皆さま  


------


# MikuMikuDB Editor

> A GUI application for generating `mod_pv_db.txt` files for Project Diva song packs.  
> English version `MikuMikuDB Editor.exe` is provided. (Developed with Python 3.12; distributed as a single `.exe`.)

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Configuration & Auto-Save](#configuration--auto-save)  
7. [Generating `mod_pv_db.txt`](#generating-mod_pv_dbtxt)  
8. [File Structure](#file-structure)  
9. [License](#license)  
10. [Acknowledgments](#acknowledgments)  

---

## Overview

This application provides a GUI for creating `mod_pv_db.txt` files for Project Diva song packs.  
- **English Version (MikuMikuDB Editor)**: All labels, menus, and dialogs are in English.  
- **Developed With:** Python 3.12  
- **Distribution:** A single Windows `.exe` executable (no `.py` source files included).  

After downloading `MikuMikuDB Editor.exe`, simply run it to launch the GUI.

---

## Features

- **English Interface**  
  - All labels, menus, and dialogs are localized in English (UTF-8).  
- **Pack Information**  
  - “Song Pack Name:” field for entering the pack name in Roman characters.  
  - “Japanese name:” field (optional) for entering the pack name in Japanese.  
- **Multi-Song Support**  
  - Songs are displayed in a tree view with columns: PV ID, Original Name, English Name.  
  - Buttons to manage the list: **Add Song**, **Edit Song**, **Delete Song**.  
- **Song Configuration**  
  - Clicking **Add Song** or **Edit Song** opens the **Configure Song** dialog, which has five tabs:  
    1. **Basic Information**  
       - **PV ID:** (e.g., `1131`)  
       - **Original name:**  
       - **English name:**  
       - **Alternative English name:** (optional)  
       - **Hiragana name:**  
       - **Romanized name:**  
       - **BPM:**  
       - **Date (YYYYMMDD):**  
       - **Sabi start time:** (chorus start time in seconds)  
       - **Sabi duration:** (chorus length in seconds)  
    2. **Difficulties**  
       - Checkboxes for **Easy**, **Normal**, **Hard**, **Extreme**, **Extra Extreme**.  
       - Each checked difficulty shows a **Level** entry (default values:  
         - Easy: `PV_LV_030`  
         - Normal: `PV_LV_055`  
         - Hard: `PV_LV_080`  
         - Extreme: `PV_LV_085`  
         - Extra Extreme: `PV_LV_095`  
         ). You can change these `PV_LV_XXX` values.  
    3. **Performers**  
       - **Selected performers:** Listbox showing added characters.  
       - **Select character:** Dropdown (combobox) listing:  
         - `MIK - Hatsune Miku`  
         - `RIN - Kagamine Rin`  
         - `LEN - Kagamine Len`  
         - `LUK - Megurine Luka`  
         - `KAI - KAITO`  
         - `MEI - MEIKO`  
         - `HAK - Yowane Haku`  
         - `NER - Akita Neru`  
         - `SAK - Sakine Meiko`  
         - `TET - Kasane Teto`  
       - **Add** button to add the selected character to the list, **Remove** button to delete a selected performer.  
    4. **Song Information**  
       - Under **Original** (in bold), fields for:  
         - **Arranger:**  
         - **Guitar Player:**  
         - **Lyricist:**  
         - **Manipulator:**  
         - **Composer/Artist:**  
         - **PV Editor:**  
       - Under **English** (in bold), fields for:  
         - **Arranger (EN):**  
         - **Guitar Player (EN):**  
         - **Lyricist (EN):**  
         - **Manipulator (EN):**  
         - **Composer/Artist (EN):**  
         - **PV Editor (EN):**  
       - All are optional; leave blank to omit.  
    5. **Audio Variants**  
       - **Configured audio variants:** Treeview with columns: **Original Name**, **English Name**, **Artist**.  
       - **Add Variant** button opens the **Configure Audio Variant** dialog with fields:  
         - **Variant name:**  
         - **English name:**  
         - **Alternative English name:** (optional)  
         - **Romanized name:**  
         - **Variant artist:**  
         - **Artist in English:**  
         - Buttons: **Accept** (save) and **Cancel** (discard).  
       - **Edit Variant** button to modify a selected variant.  
       - **Remove Variant** button to delete a selected variant.  
- **Auto-Save System**  
  - Automatically saves the current configuration every **5 minutes** into the `Autosaves/` folder as a `.pdpack` file.  
  - Keeps up to **60** autosave files; older ones are deleted when the limit is exceeded.  
- **Save / Load Configuration**  
  - **Save Configuration** button exports the current state as a `.pdpack` (JSON) to any chosen location.  
  - **Load Configuration** button opens a file dialog to select a `.pdpack` and restore pack name, song list, and settings.  
  - **Load Autosave** button shows a list of recent autosave files (most recent first) and reloads the selected one.  
- **Generate `mod_pv_db.txt`**  
  - **Generate File** button in the main window opens a save dialog (default filename `mod_pv_db.txt`).  
  - After choosing location and clicking **Save**, a UTF-8 encoded `mod_pv_db.txt` is created with all configured songs.  

---

## Requirements

- **Windows 10/11** (to run the `MikuMikuDB Editor.exe` directly).  
- Python 3.12 was used for development; end users only need the `.exe` file—no separate Python or Tkinter installation required.

---

## Installation

1. Navigate to the GitHub repository’s “Releases” page.  
2. Download the English executable **`MikuMikuDB Editor.exe`**.  
3. Double-click the downloaded `.exe` to launch the application.  
   - If Windows warns about an unknown publisher, right-click → **Properties** → check **Unblock** → **Apply**, then run again.

---

## Usage

1. **Run `MikuMikuDB Editor.exe`**.  
2. The main window (“MikuMikuDB Editor”) appears with two entry fields at the top:  
   - **Song Pack Name:** (enter the pack’s Roman-character name)  
   - **Japanese name:** (optional; enter Japanese pack name)  
3. **Managing the Song List:**  
   - Use the **Add Song** button to open the **Configure Song** dialog:  
     - **Basic Information** tab: enter **PV ID**, **Original name**, **English name**, **Alternative English name**, **Hiragana name**, **Romanized name**, **BPM**, **Date (YYYYMMDD)**, **Sabi start time**, **Sabi duration**.  
     - **Difficulties** tab: check **Easy**, **Normal**, **Hard**, **Extreme**, **Extra Extreme** as needed; for each checked difficulty, edit the **Level** (e.g., `PV_LV_080` etc.).  
     - **Performers** tab: select a character from the **Combobox** (e.g., `MIK - Hatsune Miku`) and click **Add**. To remove, select in the listbox and click **Remove**.  
     - **Song Information** tab: optionally fill in **Arranger**, **Guitar Player**, **Lyricist**, **Manipulator**, **Composer/Artist**, **PV Editor** under **Original**; optionally fill in the same fields under **English**.  
     - **Audio Variants** tab: if you need multiple audio tracks per song, click **Add Variant** to open **Configure Audio Variant**:  
       - Enter **Variant name**, **English name**, **Alternative English name** (optional), **Romanized name**, **Variant artist**, **Artist in English**, then click **Accept**. The new variant appears in the tree.  
       - To modify or delete, select the variant and click **Edit Variant** or **Remove Variant**.  
     - Once all fields are set, click **Accept** at the bottom of the **Configure Song** dialog to add the song to the list.  
   - Select an existing song in the list and click **Edit Song** to reopen and modify its settings, or click **Delete Song** to remove it.  
4. **Saving / Loading Configuration:**  
   - **Save Configuration:** Click the **Save Configuration** button, choose or create a `.pdpack` file, and click **Save**. This writes the current pack name, pack name (JP), and list of songs (with all details) into a JSON `.pdpack`.  
   - **Load Configuration:** Click **Load Configuration**, select a previously saved `.pdpack`, and click **Open**. The application restores the pack name, pack name (JP), and all songs.  
   - **Load Autosave:** Click **Load Autosave**. A dialog lists recent autosave files (with timestamps). Select one and click **Load** to restore that state.  
5. **Generating `mod_pv_db.txt`:**  
   - After adding at least one song and filling “Song Pack Name,” click **Generate File**.  
   - A save dialog appears (default filename `mod_pv_db.txt`). Choose the destination folder/name and click **Save**.  
   - Upon success, a message box shows “File generated successfully: [path]\mod_pv_db.txt”. The file is UTF-8 encoded and ready to be used in Project Diva’s custom pack.

---

## Configuration & Auto-Save

- **Auto-Save:**  
  - Every 5 minutes, if there is at least one song or a nonempty pack name, the current configuration is automatically saved as a `.pdpack` in the `Autosaves/` folder.  
  - Keeps up to 60 autosave files; old ones are deleted when the count exceeds 60.  
- **Manual Save / Load:**  
  - **Save Configuration** button allows you to export your current settings to a `.pdpack` file at any time.  
  - **Load Configuration** button lets you load any valid `.pdpack` to restore that state.  
  - **Load Autosave** button shows a list of recent autosave files (newline-separated with timestamps) for you to pick and restore.

---

## Generating `mod_pv_db.txt`

1. Confirm that **Song Pack Name** is not empty and you have at least one song in the list.  
2. Click **Generate File** in the main window.  
3. In the save dialog, accept the default `mod_pv_db.txt` or enter a new filename, choose the folder, and click **Save**.  
4. A confirmation message box appears showing the full path of the generated file. The file includes:  
   - Header section with pack name.  
   - For each song, all properties (BPM, date, script filenames, difficulty levels, performers, Sabi timing, sound filenames, song names, song info, audio variants, etc.) formatted correctly for Project Diva’s `mod_pv_db.txt`.  

---

## File Structure

```

├── LICENSE                         # MIT License
├── README.md                       # この README ファイル (English / 日本語)
├── MikuMikuDB Editor.exe           # 英語版実行ファイル
└── Autosaves/                      # 自動保存 (.pdpack) ファイルが格納されるフォルダ

```

- **`MikuMikuDB Editor.exe`**: English version executable.  
- **`Autosaves/`**: Created on first run; stores periodic `.pdpack` autosave files.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

## Acknowledgments

- Inspired by the Project Diva modding community.  
- Developed by **NyxC**.  
- Special thanks to all beta testers and contributors for their feedback.
