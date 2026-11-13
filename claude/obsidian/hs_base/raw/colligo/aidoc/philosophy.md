---
document_type: landing
description: "what the AI platform is."
sectnum: False
---

# Philosophy

The AI platform aims to facilitate the end-to-end lifecycle of delivering delightful AI experiences to Adobe's users.

Historically, the AI platform came together by merging efforts that initially focused on inference technology for the Firefly generative AI services, data processing for training Firefly models, and the AI compute platform.

`Of course, the first question is how are you helping and will plan to help achieve this :) . This section of the document is under development. More to come here in the future ...`

## Short-term vs. long-term code lifecycle

The end-to-end lifecycle of delivering AI experiences, from ideation and research to delivery, evolution, and maintenance, involves very different processes. On one hand, we have research and prototyping, where code is written that might only live for days or months. On the other hand, we have code that starts being widely used and needs to live and evolve for a long time.

Software engineering at Google [^1] refers these two sides of the spectrum as **programming** and **software engineering**, respectively. Here, we will refer to them as short-lived and long-lived code.

For short-term code, software engineering practices might be seen as hindrances, while as the timeline expands, software engineering practices become a must. As shown in the illustration below:


```{image} /aidoc/_assets/philosophy/coding-over-time.png
:width: 70%
:align: center
```

As the AI platform aims targets use cases across both sides, it chooses different solutions for each use case.

For short-lived use cases, the AI platform aims to ship our frameworks as installable software (e.g., via the Python pip package manager), following other community solutions.

For long-lived use cases, **the main goal here is that as the amount of code increases, the collective code maintenance overhead should increase sublinearly** - illustrated with the figure below. Note that code in itself is a liability, and we should strive to keep it as minimal as possible. Nevertheless, with more features, inevitably we will have more code.


```{image} /aidoc/_assets/philosophy/effort-increase.png
:width: 50%
:align: center
```

We believe that we can achieve this by having the platform code and the user code both live in a single monorepo *with the right investments*[^2].

## Why monorepo for software engineering?

We are dealing with a network of code, some managed by a single team and some by multiple teams that collectively work together. Some of these might be at the top of the dependency chain with no dependencies, while others might be at the bottom, with many dependencies.

```{image} /aidoc/_assets/philosophy/code-network.png
:width: 50%
:align: center
```

The simplest and first approach is to have each of these teams manage their own code in their own repository and tooling. This works in many situations and should be the first strategy to try.

When you focus on each individual team and ignore their dependencies on other teams, this method seems optimal.

However, the teams do depend on each other, and these dependencies create challenges as they begin to move quickly (unlike some open-source projects that can take years to implement a change). The number of teams, their members, and their codebases grow, leading to issues such as:
- If you want to make a change that spans across code managed by multiple teams, every engineer needs to get on board and learn the tools of each of the other teams. This issue worsens as the number of teams increases. Some teams might not even have members familiar with the language's tools, making it difficult to maintain minimum software engineering standards.
- As development is decoupled, a team can introduce a change that breaks another team's code. But because updates are often done lazily, the affected team might not realize the issue until they update. This problem exacerbates as the number of teams increases, leading to dependency hell[^3].

A monorepo with *proper tooling and processes* can help here. The idea is to allow all teams to use a uniform ecosystem for build, test, and other software engineering practices, including the ability to test all the code together as changes are made. At the same time, we want to minimize the overhead each team faces compared to working independently without dependencies. Granted, the overhead will never be zero, as this is not a zero-sum game. It also requires careful consideration of which workflows need to be low-overhead for each team, as we cannot target everything.


[^1]: [software engineering at google, what is software engineering?](https://abseil.io/resources/swe-book/html/ch01.html)
[^2]: Our monorepo tooling has been succesful in scaling the monorepo to service around 200 developers. However, it is being challenged to scale beyond this current usage, and thus we are planning update the tooling and processes for its next phase of scaling [FFP-14611](https://jira.corp.adobe.com/browse/FFP-14611).
[^3]: [Dependency Hell](https://en.wikipedia.org/wiki/Dependency_hell)