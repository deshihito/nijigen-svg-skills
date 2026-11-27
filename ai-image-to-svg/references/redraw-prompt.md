# 描き直しプロンプト テンプレート

元絵を添付し、`[...]` を対象に合わせて埋めて使う。英語のままが安定する。

設計原理（SKILL.md の概念に対応）：

- 保持したい性質は**漏れなく列挙**する。書かなかった性質は様式の標準形で
  埋まる（概念1）。
- 拘束は**測定できる単位**で書く：個数、割合、階調数、色の関係（概念1・4）。
- 様式カテゴリは意図して選ぶ。簡略化を強めるほど別カテゴリへ滑る
  （概念1）。本人性が階調や内部線に宿る絵では、そこを消す指定をしない
  （概念2）。

```text
Redraw this exact image as a clean flat vector illustration, as if it were
traced and rebuilt as an SVG illustration by a human designer.
Keep the same composition and identity: [保持する特徴を列挙。部品だけでなく、
目の開き具合・表情の癖・構図の切り方など、保持したい性質をすべて書く]

Simplification rules:
- Hair is a few large smooth clumps with clean curved outlines (about
  [N] clumps total), absolutely no individual hair strands, no thin lines
  inside the hair, no stray flyaway hairs.
- One single thick highlight band on the hair. No streak highlights.
- Flat colors, with at most [階調数] stepped flat tones per area.
- Bold clean outlines. No gradients, no glow effects, no texture,
  no watermark text. Decorative motifs: at most [N] large flat shapes.
- Small essential face parts (nose, mouth) are present and drawn BOLD and
  clearly visible, never pale or subtle - they must survive a vector trace.
  [例: the nose is a single tiny dot in a muted skin-shadow color,
  low saturation]
- Eyes: about [N]% of the iris visible. Do not round the eyes, do not
  open them wider, do not narrow them to slits.
- Expression: keep [表情の癖を文章で]. Do not normalize it into a generic
  expression.
- Composition: keep the original framing exactly. [フレーム端で切れている
  要素がある場合: elements cropped by the frame edges stay cropped;
  do not pull the whole subject into the frame, do not add margins.]
- Adjacent parts that must stay separate are clearly separated in value:
  [例: skin is visibly warmer and deeper than the pale hair next to it,
  so the two never merge into one color.]
- Every shape should look like a smooth vector path with few anchor points.
- Clean and readable even at small icon size.
```

## 部位ごとの配分

一律ではなく、部位ごとに予算を変える（概念4）。書き方の例：

- 本人性の核だけ高予算：`the eyes keep full detail: iris in 3 tones,
  dark pupil, two highlights`（目だけに付ける）
- 濃淡が情報を持つ部位：部位ごとに階調数を書く
  `hair in 4 stepped tones, skin in 3, the interior scene in 8 stepped
  tones; overlapping transparent areas are drawn as solid panels of real
  color, never as transparency`
- 参照の仕方を部位で分ける（修正生成時）：
  `Keep [コピーさせる部位] exactly as they are. Only redraw [部位]:
  for it do NOT copy the interior details of the source; reference only
  its outer silhouette and its color.`

## ずれたときの直し方（概念への対応で考える）

- 何かが標準形に寄った（目・表情・構図・色）→ その性質が未指定だった
  ということ。保持リストに測定できる形で追加する（概念1）。
- ディテールが残る → 形容詞ではなく、数（房・モチーフ・階調）の上限を
  下げて縛る（概念1・3）。
- 色の着地点がずれた → 生成で直さない。トレース後に fill を目標RGBへ
  置換する（概念7）。部位単独ではなく隣接部位との関係で目標を決める
  （概念5）。
- 小パーツがトレースで消えた → 生成で直さない。SVG側に実測座標で
  足す（概念5・7）。
- 文字が崩れた → 文字はパス化しない。内側を無地にしてトレースし、
  `<text>` で置く（概念2・7）。
