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
- Coloring grammar: NO shadow tones by default - one single flat tone
  per area, form carried by the lines. Add a shadow only where its
  shape itself carries information (under the chin, the inner mass of
  the hair), as one sharp designed shape that follows the form -
  crescent cuts and angular wedges with clean edges, never soft blobs.
- Blush is drawn as diagonal hatch strokes on the cheeks, never as
  solid shapes or soft smudges.
- Strong consistent outline linework defines every boundary; flat color
  only fills inside the lines.
- BOUNDARY RULE: every region is a closed shape enclosed by the outline;
  no two flat fills ever touch each other directly - an outline always
  separates them. Silhouette details (a profile nose bump, lips) are
  drawn as part of the outline line, never as bumps of a color fill.
- Lighting is translated into normal local colors: skin is drawn in
  normal skin tones, never tinted by colored ambient light in the scene.
- Limited palette: few hues, with clear value separation between
  neighboring parts so no two adjacent areas can merge.
- Bold clean outlines. No gradients, no glow effects, no texture,
  no watermark text. Decorative motifs: at most [N] large flat shapes.
- Small essential face parts (nose, mouth) are present and drawn BOLD and
  clearly visible, never pale or subtle - they must survive a vector trace.
  [顔の扱いの例: the face is one single flat skin tone with no shadow on
  the face; the nose is a single tiny dot in the dark outline color.
  影色で置く場合は彩度を落とす。点の大きさは顔幅の約2％が上限
  （概念8・手順5）]
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
- 濃淡が情報を持つ部位だけ、文法の例外として階調数を書く（概念8）
  `hair in 4 stepped tones, skin in 3, the interior scene in 8 stepped
  tones; overlapping transparent areas are drawn as solid panels of real
  color, never as transparency`
- 参照の仕方を部位で分ける（修正生成時）：
  `Keep [コピーさせる部位] exactly as they are. Only redraw [部位]:
  for it do NOT copy the interior details of the source; reference only
  its outer silhouette and its color.`

## 様式参照画像を使う場合

目標の塗りを持つ絵を2枚目に添付し、`using the COLORING GRAMMAR of
the second image` と指定すると、影の形・線の扱い・配色の文法（概念8）が
言葉より正確に移る。文法の指定と予算の指定は別軸なので、参照画像を
使っても予算（房の数など）は併記する。注意：参照画像からは内容
（背景モチーフ、配色、小物）も漏れてくる。漏れが困る場合は使わない。

使い方には2つの水準がある。単純さの水準だけを借りる（軽さ優先）と、
質の高い参照を丸ごと真似る（質優先）。丸ごと真似ると顔の扱いや表情
まで移るので、表情を保持したい場合は保持リストで明示する。

## 背景をキー色にする場合（概念9）

主題と背景の分離が要る場合は、背景をキー色の単色で描かせる：

```text
BACKGROUND: completely plain solid chroma-key green (#00B140) edge to
edge, no motifs, no gradient; the green must not appear anywhere on
the character.
```

キー色は主題に含まれない色を選ぶ。背景モチーフは別レイヤーで用意し、
キーアウト後に合成する。

## ずれたときの直し方（概念への対応で考える）

- 何かが標準形に寄った（目・表情・構図・色）→ その性質が未指定だった
  ということ。保持リストに測定できる形で追加する（概念1）。
- ディテールが残る → 形容詞ではなく、数（房・モチーフ・階調）の上限を
  下げて縛る（概念1・3）。
- 色の着地点がずれた → 生成で直さない。トレース後に fill を目標RGBへ
  置換する（概念7）。部位単独ではなく隣接部位との関係で目標を決める
  （概念5）。肌色のブレは参照と成果物の頬の中央値を実測し、ズレた
  チャネルだけ寄せる。
- 輪郭の凹凸（横顔の鼻など）がトレースで落ちた → 面の輪郭としてでは
  なく、線として描き直す（境界の明示、概念8）。
- 小パーツがトレースで消えた → 生成で直さない。SVG側に実測座標で
  足す（概念5・7）。
- 文字が崩れた → 文字はパス化しない。内側を無地にしてトレースし、
  `<text>` で置く（概念2・7）。
