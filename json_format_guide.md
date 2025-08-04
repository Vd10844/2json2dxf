## 📄 `JSON_FORMAT_GUIDE.md`

> **Title**: JSON Format Guide for 2json2dxf
> **Purpose**: Defines how to structure JSON files used to generate DXF drawings using `2json2dxf`.

---

### 🔧 Purpose

This guide is for **JSON creators** working on the `2json2dxf` project.
It explains how to define **drawing standards** and **drawing entities** in JSON so they can be parsed and rendered into `.dxf` files using Python and [ezdxf](https://github.com/mozman/ezdxf).

---

## 📁 Files You Must Provide

You must create **two JSON files**:

1. `standards.json` – defines CAD drawing standards (layers, units, text styles, etc.)
2. `drawing.json` – defines the actual entities (lines, circles, text, etc.) to be drawn

---

## 🧰 1. `standards.json` Format

```json
{
  "drawing_metadata": {
    "units": "mm"
  },
  "default_text_style": "STANDARD",
  "layers": {
    "LayerName1": {
      "color": 1,
      "linetype": "Continuous"
    },
    "LayerName2": {
      "color": 3
    }
  }
}
```

### Fields:

| Field                | Type   | Description                                                             |
| -------------------- | ------ | ----------------------------------------------------------------------- |
| `drawing_metadata`   | object | Optional, contains global drawing info like units                       |
| `units`              | string | `"mm"`, `"inches"`, `"feet"`, `"cm"`, `"m"`                             |
| `layers`             | object | Layer dictionary. Key = layer name, value = color, linetype             |
| `default_text_style` | string | Optional text style name used for `text` entities (default: "STANDARD") |

---

## ✏️ 2. `drawing.json` Format

```json
{
  "entities": [
    {
      "type": "line",
      "start": [0, 0],
      "end": [100, 0],
      "layer": "LayerName1"
    },
    {
      "type": "circle",
      "center": [50, 50],
      "radius": 20,
      "layer": "LayerName2"
    }
  ]
}
```

### ✅ Supported Entity Types


| Type               | Required JSON fields                                       |
| ------------------ | ---------------------------------------------------------- |
| `line`             | `start`, `end`                                             |
| `circle`           | `center`, `radius`                                         |
| `arc`              | `center`, `radius`, `start_angle`, `end_angle`             |
| `ellipse`          | `center`, `major_axis`, `ratio`                            |
| `polyline`         | `points` (list)                                            |
| `point`            | `position`                                                 |
| `text`             | `content`, `position`, `height`                            |
| `mtext`            | `content`, `position`, `height`                            |
| `dimension_linear` | `start`, `end`, `dim_line_position`, `text`, `text_height` |
| `insert`           | `block_name`, `position`                                   |
| `hatch`            | `boundary` (closed loop of points)                         |
| `solid`            | `points` (3 or 4 points)                                   |


---

### Optional Common Fields:

* `layer`: string – Name of layer (must match one from `standards.json`)
* `color`: int – If omitted, layer’s color is used

---

## ⚠️ Limitations & Rules

### ❗ Known Limitations:

| Limitation                        | Workaround                                      |
| --------------------------------- | ----------------------------------------------- |
| No 3D geometry                    | Only 2D drawing entities are supported          |
| No blocks/hatching yet            | Add future support or flatten manually          |
| No unit conversion in script      | Units must be set correctly in `standards.json` |
| Style names must exist in AutoCAD | Use default styles like `"STANDARD"`            |
| Fails silently on missing fields  | Always double-check required fields per entity  |

---

### 🔍 Validation Tips:

* Use an online JSON validator like [jsonlint.com](https://jsonlint.com)
* Make sure every entity:

  * Has a `"type"`
  * Includes all required fields
  * Refers only to layers that exist in `standards.json`

---

### 🧪 Test Sample

Use this minimal valid pair to test:

**`standards.json`**

```json
{
  "drawing_metadata": { "units": "mm" },
  "layers": { "main": { "color": 1 } }
}
```

**`drawing.json`**

```json
{
  "entities": [
    { "type": "line", "start": [0, 0], "end": [100, 0], "layer": "main" }
  ]
}
```

---

## ✅ Best Practices

* Use **consistent layer names**
* **Avoid units in coordinates** — the unit system is set in `standards.json`
* Keep your JSON clean and avoid trailing commas
* Use `"type"` in lowercase (e.g. `"line"`, `"circle"`)

