# Image Optimizer
Dockerized Responsive image resizer and optimizer service that processes images on the fly.


## Query Parameter Description
* tag: tag optimizer. (example: `thumb`)
* q: export image quality
* type: export image resizing type. `crop` | `resize` | `force_resize`
* size: export image size. (pattern: `width`x`height`)


## Note
* if you send `tag` parameter, skip `q`, `type` and `size` parameter
* if you want send request by `get` method, you should add `url` query parameter in request
and if you want send request by `post` method you should set `file` key in form parameter

* if you want send request by `post` method, you can also set `q`, `type` and `size` parameter in form

## Example Requests
```
http://127.0.0.1:5000/?q=70&type=crop&size=200x250&url=https://www.w3schools.com/html/pulpitrock.jpg
http://127.0.0.1:5000/?tag=thumb&url=https://www.w3schools.com/html/pulpitrock.jpg

http://127.0.0.1:5000/info?url=https://www.w3schools.com/html/pulpitrock.jpg
```