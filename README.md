# Real-ESRGAN_CreateMovieHelper


# To ENG

Simply automation tool for Real-ESRGAN.

# To JPN

[どんなツール？]
○realesrgan-ncnn-vulkanの処理を簡単操作&自動で動画のアップコンバートを行えるようにするべく作成された補助ツール。
・CUIのコマンド操作に不慣れな方が操作しても簡単に作成できるように、対話形式でモデル指定が可能。
・Configを用いて予めお好みの設定を用意した上で使用できます。
・自前でffmpegのコマンドを打つCUI特有の面倒さ削減にも一役買うのではないかなと思います。

[実装している処理一覧]
・読み込んだ動画ファイルのフレームレートを確認し、連番連結時に使用。
・前に行った処理にて作られた連番画像があれば、警告を行う。
・なにかしらの不具合が発生して連番画像が作成されなかった場合は、エラー文。


[現在の課題]
v1.0現在、realesrgan-ncnn-vulkan.exeで入力を行えるコマンドの最低限のみ実装しています。
ちょくちょくバージョン更新して最終的にはなんでもconfigで設定できるようにしたいです。
ぶっちゃけここまでならbatchでできるレベルのことを実装しているだけなので、もう少し凝った処理も入れてみたいです。
不慣れな方を対象にするならば、GUI化も考慮すべきですので、技術的に可能であれば将来的に行います。
Gitって…どうやって使うの…？
日本語ノンネイティブの方向けに英語版でリリースしたいが、簡単に切り替えできる方法はないか模索中。

@file Real-ESRGAN-NV-CreateMovieHelper
@brief Real-ESRGANで楽に動画化するためのものです。
@author Aerin the Lion(aka. Lost History)
@date 12.29.2021

※※※ツールの使用は自己責任でお願いいたします。※※※
