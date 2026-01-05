#!/bin/bash

# Create comprehensive directory structure for Kakuro KDP Publishing Project

# Source code directories
mkdir -p src/puzzle_generation
mkdir -p src/pdf_generation
mkdir -p src/layout
mkdir -p src/utils
mkdir -p src/validation

# Tests
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures

# Assets
mkdir -p assets/fonts
mkdir -p assets/images/logos
mkdir -p assets/images/graphics
mkdir -p assets/templates/covers
mkdir -p assets/templates/interiors
mkdir -p assets/templates/instructions

# Market Research
mkdir -p research/competitors
mkdir -p research/keywords
mkdir -p research/pricing
mkdir -p research/trends

# Output/Deliverables
mkdir -p output/puzzles/beginner
mkdir -p output/puzzles/intermediate
mkdir -p output/puzzles/expert
mkdir -p output/books/interiors
mkdir -p output/books/covers
mkdir -p output/books/final
mkdir -p output/previews
mkdir -p output/marketing

# KDP Listings
mkdir -p kdp/metadata
mkdir -p kdp/descriptions
mkdir -p kdp/keywords
mkdir -p kdp/categories

# Documentation
mkdir -p docs/api
mkdir -p docs/guides
mkdir -p docs/examples

# Configuration
mkdir -p config/book_specs
mkdir -p config/difficulty_profiles

# Data
mkdir -p data/generated_puzzles
mkdir -p data/puzzle_cache
mkdir -p data/analytics

# Scripts
mkdir -p scripts/batch_generation
mkdir -p scripts/quality_control
mkdir -p scripts/deployment

# Portfolio tracking
mkdir -p portfolio/published
mkdir -p portfolio/in_progress
mkdir -p portfolio/planned

echo "Directory structure created successfully!"
