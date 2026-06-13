# System libraries WeasyPrint needs to render PDFs on Replit's Nix environment.
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.pango          # text layout (WeasyPrint core dep)
    pkgs.cairo          # 2D rendering
    pkgs.gdk-pixbuf     # image handling
    pkgs.glib
    pkgs.libffi
    pkgs.fontconfig     # font discovery
    pkgs.freetype
    pkgs.harfbuzz
  ];
}
