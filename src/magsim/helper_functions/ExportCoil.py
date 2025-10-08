import ezdxf
import math

from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget


class CoilFile():
    def __init__(self, coil, parent: QWidget | None = None):
            self.coil     = coil
            self.parent   = parent

    def generate_dxf(self, filename: str):
        doc = ezdxf.new(dxfversion='R2010')

        if "TopLayer" not in doc.layers:
            doc.layers.new(name="TopLayer", dxfattribs={"color": 1})

        msp = doc.modelspace()
        
        
        if self.coil.coil_type == 'circular':
            length = self.coil.length - (2 * self.coil.edge_clearance)      # mm
            width = self.coil.width - (2 * self.coil.edge_clearance)        # mm
            num_loops = self.coil.num_loops                             # int
            trace_w = self.coil.trace_width / 39.3701                   # mm
            min_spacing = self.coil.min_spacing / 39.3701               # mm

            cx = (self.coil.width  / 2)    # mm
            cy = (self.coil.length / 2)    # mm

            min_radius = min(length, width) / 2
            theta = 0.0
            theta_end = 2 * math.pi * num_loops
            dtheta = math.radians(0.1)  # small step; smaller = smoother

            pts = []

            while theta <= theta_end:
                hypotenuse = (min_radius - ((trace_w + min_spacing) * (theta / (2 * math.pi))))  # radius at current theta
                x = hypotenuse * math.cos(theta)
                y = hypotenuse * math.sin(theta)
                pts.append((x + cx, -y + cy))
                theta += dtheta

            msp.add_lwpolyline(
                pts,
                format="xy",
                dxfattribs={"layer": "TopLayer", "const_width": trace_w},
            )

        doc.saveas(filename)

    def on_export_dxf(self):

        fname, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save DXF",
            "magsim_coil.dxf",                            # default name
            "DXF Files (*.dxf);;All Files (*)"
        )
        if not fname:
            return  # user cancelled

        if not fname.lower().endswith(".dxf"):
            fname += ".dxf"

        try:
            self.generate_dxf(fname)
        except Exception as e:
            QMessageBox.critical(self.parent, "DXF Export Failed", str(e))
            return

        QMessageBox.information(self.parent, "DXF Export", f"Saved to:\n{fname}")