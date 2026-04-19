#!/bin/bash

# Build script for wisdom courses
# Combines all module files into a single index.html

# Check if we're in a course directory
if [ ! -f "_base.html" ]; then
    echo "Error: _base.html not found. Are you in a course directory?"
    exit 1
fi

# Read the base template
BASE=$(cat _base.html)

# Read all modules in order
MODULES=""
for module in modules/*.html; do
    if [ -f "$module" ]; then
        MODULES+="$(cat "$module")"
        MODULES+=$'\n'
    fi
done

# Read footer
FOOTER=$(cat _footer.html)

# Combine everything
HTML="${BASE/MODULES_PLACEHOLDER/$MODULES$FOOTER}"

# Write to index.html
echo "$HTML" > index.html

echo "✅ Built index.html successfully!"
echo "📖 Open index.html in your browser to view the course."