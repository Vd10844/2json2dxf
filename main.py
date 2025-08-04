import json
import os
import sys
import ezdxf

DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "output")


def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[❌] Failed to load JSON from {path}: {e}")
        sys.exit(1)


def create_layers(doc, layers):
    for name, props in layers.items():
        try:
            doc.layers.add(
                name=name,
                color=props.get("color", 7),
                linetype=props.get("linetype", "Continuous")
            )
        except Exception as e:
            print(f"[⚠️] Failed to create layer '{name}': {e}")


def draw_entity(entity, msp, default_style):
    etype = entity.get("type", "").lower()
    layer = entity.get("layer", "0")

    try:
        match etype:
            case "line":
                msp.add_line(entity["start"], entity["end"], dxfattribs={"layer": layer})

            case "circle":
                msp.add_circle(entity["center"], entity["radius"], dxfattribs={"layer": layer})

            case "arc":
                msp.add_arc(entity["center"], entity["radius"],
                            entity["start_angle"], entity["end_angle"],
                            dxfattribs={"layer": layer})

            case "polyline":
                msp.add_lwpolyline(entity["points"], dxfattribs={"layer": layer})

            case "point":
                msp.add_point(entity["position"], dxfattribs={"layer": layer})

            case "ellipse":
                msp.add_ellipse(
                    center=entity["center"],
                    major_axis=entity["major_axis"],
                    ratio=entity.get("ratio", 0.5),
                    start_param=entity.get("start_param", 0),
                    end_param=entity.get("end_param", 6.28),
                    dxfattribs={"layer": layer}
                )

            case "text":
                txt = msp.add_text(entity["content"], dxfattribs={
                    "height": entity["height"],
                    "rotation": entity.get("rotation", 0),
                    "layer": layer,
                    "style": default_style
                })
                txt.dxf.insert = tuple(entity["position"])

            case "mtext":
                mtext = msp.add_mtext(entity["content"],
                                      dxfattribs={"height": entity["height"], "layer": layer})
                mtext.set_location(entity["position"])

            case "dimension_linear":
                msp.add_line(entity["start"], entity["dim_line_position"], dxfattribs={"layer": layer})
                msp.add_line(entity["end"], entity["dim_line_position"], dxfattribs={"layer": layer})
                dim_txt = msp.add_text(entity["text"], dxfattribs={"height": entity["text_height"], "layer": layer})
                dim_txt.dxf.insert = tuple(entity["dim_line_position"])

            case "bullet_point":
                msp.add_circle(center=entity["position"], radius=entity["height"] / 2, dxfattribs={"layer": layer})
                label = msp.add_text(entity["label"], dxfattribs={"height": entity["height"], "layer": layer})
                label.dxf.insert = tuple(entity["position"])

            case "solid":
                msp.add_solid(points=entity["points"], dxfattribs={"layer": layer})

            case "hatch":
                hatch = msp.add_hatch(dxfattribs={"layer": layer})
                hatch.paths.add_polyline_path(entity["boundary"], is_closed=True)
                hatch.set_pattern_fill(entity.get("pattern", "SOLID"), scale=entity.get("scale", 1.0))

            case "insert":
                msp.add_blockref(name=entity["block_name"], insert=entity["position"], dxfattribs={"layer": layer})

            case _:
                print(f"[⚠️] Unknown entity type: {etype}. Skipping.")

    except Exception as e:
        print(f"[❌] Failed to draw entity '{etype}': {e}")


def generate_dxf(standards, drawing, output_path):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    layers = standards.get("layers", {})
    default_style = standards.get("default_text_style", "STANDARD")
    metadata = standards.get("drawing_metadata", {})

    create_layers(doc, layers)

    for entity in drawing.get("entities", []):
        draw_entity(entity, msp, default_style)

    # Set units
    units_map = {"inches": 1, "feet": 2, "mm": 4, "cm": 5, "m": 6}
    doc.header["$INSUNITS"] = units_map.get(metadata.get("units", "").lower(), 0)

    doc.saveas(output_path)
    print(f"[✅] DXF saved to: {output_path}")


def main():
    print("📌 2jason2dxf | JSON → DXF Generator")

    standards_path = input("📁 Path to standards JSON: ").strip()
    drawing_path = input("📁 Path to drawing JSON: ").strip()

    standards = load_json(standards_path)
    drawing = load_json(drawing_path)

    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
    drawing_name = os.path.splitext(os.path.basename(drawing_path))[0]
    output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"{drawing_name}.dxf")

    generate_dxf(standards, drawing, output_path)


if __name__ == "__main__":
    main()
