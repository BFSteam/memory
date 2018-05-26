#!/bin/bash
for file in ./*.svg
do
  inkscape -D -z --file="$file" --export-pdf="${file%.svg}.pdf" --export-latex
  echo "${file%.svg}.pdf"
done
