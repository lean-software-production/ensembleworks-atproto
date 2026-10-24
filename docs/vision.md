Social coding for the AI age. Bluesky for code.

The idea is to build an ATProto lexicon and PDS for sharing coding agent sessions between people. 

This should allow me to share specific sessions (or all sessions in a project folder) with collaborators on the network so that they can at least read them. Ideally they'll also be able to participate, the same way as I can partcipate in a thread in bluesky, within safey bounds of remote execution.

I'd like to be able to see a feed of all activity on a given team.

We can use [Groups](https://atproto.com/blog/atmospheric-groups-intro) to allow for privacy within teams/companies.

Ideally this will be harness agnostic, with flexible harnesses like [pi](https://pi.dev) and [bb](https://getbb.app) being supported first. BB support will require a plugin and potentially maintaining a fork, at least temporarily. Pi support will require an extension.

Implementation should probably be in Typescript to allow compatability with BB and Pi but we could also interface
via a CLI in Rust or Go, or use a docker container for deploying the PDS.

