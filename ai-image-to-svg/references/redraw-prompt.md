# 描き直しプロンプト テンプレート

元絵を添付し、`[...]` を対象に合わせて埋めて使う。英語のままが安定する。

```text
Redraw this exact image as a clean flat vector illustration, as if it were
traced and rebuilt as an SVG illustration by a human designer.
Keep the same composition and identity: [保持する特徴を列挙。例: silver-grey
bob hair, bright pink spiral eyes, small fang smile, black choker with buckle,
hand touching the chin, vivid flat pink background].

Simplification rules:
- Hair is a few large smooth clumps with clean curved outlines (about 7 clumps
  total), absolutely no individual hair strands, no thin lines inside the hair,
  no stray flyaway hairs.
- One single thick highlight band on the hair. No streak highlights.
- Flat colors only, with at most one flat shadow tone per area.
- Bold clean outlines. No gradients, no glow effects, no sparkles (or at most
  [N] large flat decorative shapes), no sketchy hatching, no texture,
  no watermark text.
- The nose is a single tiny dot in a muted skin-shadow color (low saturation,
  NOT pink, NOT red). Do not omit it.
- Eyes: keep the original openness - about [85]% of the iris visible
  [半開きなら 70% 前後]. Do not round the eyes, do not open them wider,
  do not make them half-closed slits either.
- Expression: keep [表情の癖。例: smug half-lidded gaze, asymmetric smirk].
  Do not normalize it into a generic cute smile.
- Composition: keep the original framing exactly. [髪などがフレーム端で
  切れている場合: the hair is cropped by the top and side edges of the frame;
  do not pull the whole head into the frame, do not add margins.]
- Face parts (nose, mouth lines, blush) are drawn BOLD and clearly visible,
  never pale or subtle - they must survive a vector trace.
- Skin is a clearly warm tone, visibly warmer and deeper than any white or
  pale hair next to it, so the two never merge into one color.
- Every shape should look like a smooth vector path with few anchor points.
- Clean and readable even at small icon size.
```

## 抽象度と階調の指定（部位ごと）

一律の簡略化ではなく、部位ごとにダイヤルを指定する：

- 抽象度・中（既定）：`MEDIUM abstraction, up to 4 stepped flat tones per area`
- 抽象度・強（アイコン用途）：`up to 2-3 tones, fewer clumps (about 5)`
- 階調モード（濃淡が主題の絵）：部位ごとに階調数を書く
  `hair in 4 stepped tones, skin in 3, the bubble interior in 8 stepped tones;
  overlapping transparent areas are drawn as solid stained-glass panels of
  real color, never as transparency`
- 本人性の核（目など）だけ高予算にする：`the eyes keep full detail:
  iris in 3 tones, dark pupil, two highlights` を目だけに付ける

## 部位ごとに参照モードを変える場合（2回目以降の修正生成）

保持したい部位と簡略化したい部位が混在するときは、編集として部位別に書く：

```text
Edit this image with per-part reference rules.
Keep [顔・目・アクセサリ] exactly as they are.
Only redraw [髪]: for the hair do NOT copy the interior details of the source;
reference only its outer silhouette and its color. [予算指定を続ける]
```

## 調整の指針

- 髪の線が残る → 房の数の上限を下げる、「no lines inside the clumps」を先頭に置く
- 本人性が崩れる → 保持リストに崩れた特徴を明示して追加する（最大でも数個まで）
- 装飾が残る → 「sparkles」ではなく形（star shapes）で数えて上限を付ける
- 目が全開／細目に振れる → 形容詞をやめ、虹彩の露出％で指定し直す
- 表情が無難になる → 表情の癖（視線・笑いの形）を保持リストに文章で入れる
- 全体が画面に収まる → 「フレーム端で切れたまま、余白を作るな」と構図を明示する
- 色が薄すぎ／濃すぎ → 再生成しない。トレース後にSVGの fill を目標RGBへ置換する
- 鼻・口がトレースで消えた → 再生成しない。SVG側に実測座標で部品として足す
