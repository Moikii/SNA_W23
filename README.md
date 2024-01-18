# Community Detection in Social Networks

## Overview

This project, conducted by Group 6 in the course Social Network Analysis at the TU Wien, explores community detection within social networks. By analyzing user comments on various topics, we aim to uncover patterns in social interactions and community formation. The project focuses on questions related to topic correlation, subtopic categorization, and gender distribution within these communities.

## Methodology

### Building the Graph

- Topics for analysis were selected based on user comments.
- Users with fewer than 5 comments were excluded.
- User interactions were quantified using the Intersection over Minimum (IOM) method.

$$
                IOM(u, v) = \frac{|A(u)\cap A(v)|}{\min\left(|A(v)|, |A(v)|\right)}
$$


### Algorithms Evaluated

- Girvan-Newman
- Weighted Girvan-Newman
- Maximum Modularity
- Label Propagation
- Louvain Communities

Performance was measured in terms of runtime and modularity. The experiments were conducted on the Jupyterhub provided by the lecture-team.

### Community Detection

- Communities were analyzed to determine correlation with topics, recognition of subtopics, and gender distribution.
- Maximum modularity method was used for effective community detection.
- Focus was placed on specific topics to enhance community distinction.

## Key Findings

- Communities often reflect user interest in specific topics and subtopics.
- Distinct patterns in gender distribution within communities were observed.
- Analysis of all topics together was challenging; focused topic analysis yielded clearer community structures.

## Project Structure

- `./src`: Contains notebooks for various subtopic combinations and algorithm evaluations.
- `./plots`: Contains plots and visualizations generated from the notebooks.
- Key notebooks include `fh_community_sport.ipynb`, `mm_community_kultur_gesundheit.ipynb`, and others for specific topic combinations.

## Running the Project

1. Install dependencies listed in `requirements.txt`.
2. Explore the notebooks in `./src` to run specific analyses or evaluate algorithms.

## Contributors

- Hartmann Fabian (11824496)
- Moik Matthias (11810738)
- Stöckler Isabella (11812328)
- Unruh Jonas (12331457)
- Ziegler Daniel (11909868)
