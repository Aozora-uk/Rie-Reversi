# Ai-Reversi

Reversi bot for Misskey v12 &amp; v13

初心者がつくったバグだらけのコードです。

藍のスクリプトに組み込まれるのではなく、完全に独立して動きます。https://mi.rhyme.ml/@ai@mi.rhyme.ml

## インストール方法メモ

依存 : python3, pip, g++
```
$ git clone https://github.com/dvorak-lya/Ai-Reversi.git
$ cd Ai-Reversi
$ git clone https://github.com/Nyanyan/Egaroucid.git

```

ここで次のような config.json を作成する

```
{
	"domain": "あなたのインスタンスuriを入力 (https://と最後の/なし)",
	"token": "アクセストークンを入力",
	"maxlevel": "レベルのMAX値。0〜60の範囲。あまり上げ過ぎると負荷、時間、安定性に悪影響",
	"defaultlevel": "レベルを指定しなかったときの値。0〜60の範囲。ほどほどに"
}
```

Engaroucidをビルド

```
$ cd Egaroucid/src

// ARMの場合(Raspberry Pi)
$ g++ -O2 Egaroucid_console.cpp -o Egaroucid_for_Console.out -mtune=native -march=native -pthread -std=c++17 -Wall -Wextra -DHAS_ARM_PROCESSOR -DHAS_NO_AVX2

//X64の場合
$ g++ -O2 Egaroucid_console.cpp -o Egaroucid_for_Console.out -mtune=native -march=native -pthread -std=c++17 -Wall -Wextra

$ cd ../../
```

Pythonの依存パッケージをインストール

```
$ pip install Misskey.py websockets
```

起動！

```
$ python3 main.py
```

## License

MIT

注意 : submoduleのEgaroucidはGPLライセンスです
