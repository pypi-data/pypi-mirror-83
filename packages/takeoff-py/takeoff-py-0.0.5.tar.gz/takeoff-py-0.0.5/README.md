![TakeOff](logo-small.png)

# Takeoff
A Python toolset to launch full stack, web and mobile projects

[![CircleCI](https://circleci.com/gh/themarceloribeiro/takeoff-py.svg?style=svg)](https://app.circleci.com/pipelines/github/themarceloribeiro/takeoff-py)

```
pip install takeoff-py
```

Once installed you can use the generator to start building

## Web: Django Support

### New Project

Start by creating a new project. You will be asked for django admin credentials.

```
takeoff-generate web:project blog
```

### Generate models

For model generation:

```
takeoff-generate web:model blog category name:string summary:text
```

```
takeoff-generate web:model blog post category:belongs_to title:string summary:text contents:text drafted_at:datetime published:boolean 
```

### Generate web resources

After your model exists, you can create the web resource (standard index/show/create/edit functions)

```
takeoff-generate web:resource blog category
```

```
takeoff-generate web:resource blog post
```

### Generate user authentication

User authentication is also supported by a generator

```
takeoff-generate web:authentication blog
```