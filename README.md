# ExcelBOMComparison

Intended for work at WestRock company, comparing the MBOM within IFS to the Inventor BOM.

Thoughts on how to implement without using del operator. Instead, change all values that are the same to a specific character, like "?". In this way, we can then iterate through the list afterwards and delete all of those specific characters.
