# Ai-Reversi

Reversi bot for Misskey v12 &amp; v13

初心者がつくったバグだらけのコードです。

藍のスクリプトに組み込まれるのではなく、完全に独立して動きます。https://mi.rhyme.ml/@ai@mi.rhyme.ml

## インストール方法メモ

依存 : python3, pip
```
$ git clone https://github.com/dvorak-lya/reversi-ai
$ git submodule init
$ git submodule update

// main.py のインスタンス名とトークンを書き換える

$ cd Egaroucid/src

// ARMの場合(Raspberry Pi)
$ g++ -O2 Egaroucid_console.cpp -o Egaroucid_for_Console.out -mtune=native -march=native -pthread -std=c++17 -Wall -Wextra -DHAS_ARM_PROCESSOR -DHAS_NO_AVX2

//X64の場合
$ $ g++ -O2 Egaroucid_console.cpp -o Egaroucid_for_Console.out -mtune=native -march=native -pthread -std=c++17 -Wall -Wextra

$ cd ../../
$ pip install Misskey.py websockets
$ python3 main.py
```

## License

MIT

注意 : submoduleのEgaroucidはGPLライセンスです
