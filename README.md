# 食事する哲学者

哲学者が食事をします．

![哲学者達](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/An_illustration_of_the_dining_philosophers_problem.png/231px-An_illustration_of_the_dining_philosophers_problem.png)

図は5人の哲学者と5つのフォークがあることを表しています．
- 哲学者は左右にあるフォーク2本を使ってスパゲッティを食べます．
- 哲学者はフォークを1本ずつしか持ち上げることができません．
- 哲学者同士で会話を行わないためフォークのデッドロックが発生するかもしれません．

並行性プロセスの問題です．

# Chandy-Misraの解法

哲学者が何人であっても，フォークが何本であっても可能な方法です．

- フォークに状態`dirty`と`clean`を割り当てる様にします．初期状態は`dirty`です．
- フォークを持ちたいとき，自分が使うフォーク全てに対して要求メッセージを送信します．
- 要求されたフォークの状態が`dirty`なら`clean`にし，そのフォークを持つ哲学者がフォークを手放します．
- 食事が終わるとフォークは`dirty`状態になります(次に思索を始めます)．他の哲学者にフォークを要求されたら状態を`clean`にします．

# 構成

```
.
├── README.md # このファイル
├── prob.py   # 食事する哲学者のシミュレーション(デッドロックする可能性あり)
└── solve.py  # Chandy-Misraの解法を取り入れたシミュレーション(デッドロックしない)
```

# 実行方法

Python3であれば動きます．

```
$ chmod +x prob.py solve.py
$ ./prob.py

$ python3 solve.py
```

表示し続けるので，終了したいときは`Ctrl-C`で`KeyboardInterrupt`を発行して下さい．

