# Vision Rat Brain
This repository contains the supporting code for publications and projects done by Jose G. Perez

It is not ready for public use yet.
Expect it to be complete by the end of May 2018 with an installation guide and explanations.

Any questions may be directed to me via pull requests.

## Getting Started

Here's a breakdown of all the projects included in this repository

### Main projects 
* dataset/
    * Used to preprocess (crop, resize, compress) atlas images into NPZ files for use in other projects 
* feature_matching_v1/
    * Proof of concept used for region matching using SIFT and RANSAC
    * http://www.abstractsonline.com/pp8/#!/4376/presentation/4332
* feature_matching_v2/
    * Region matching improved with custom RANSAC algorithm
* feature_matching_v3/
    * Whole image matching using SIFT and dynamic programming to derive plate correspondences
    * https://www.frontiersin.org/articles/10.3389/fnsys.2018.00007/abstract
### Side projects
* auto_encoder/
    * Deriving atlas correspondences using AE 
* matching_networks/
    * Deriving atlas correspondences through image similarities using matching networks
* siamese_networks/
    * Deriving atlas correspondences through image similarities using matching networks

### Prerequisites

### Installing

## Contributing

Please read [CONTRIBUTING.md](http://github.com/DeveloperJose/Vision-Rat-Brain) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/DeveloperJose/Vision-Rat-Brain/tags). 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

