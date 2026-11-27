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
- The nose is a single tiny dot. Do not omit it, do not draw it larger.
- Every shape should look like a smooth vector path with few anchor points.
- Clean and readable even at small icon size.
```

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
