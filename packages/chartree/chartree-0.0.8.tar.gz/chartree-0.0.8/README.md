# chartree
Grow your own trees on a monospace grid. Choose the material (unicode) for your tree as well as the hue of the sky (also unicode). Heaps of other parameters as well!

## Example
```python
import chartree as ct
w = ct.Ecosystem(material='7', background='.')

# Grows a new tree, different each time.
w.grow(n_iter=50, ang_mean=40, ang_range=10)
```
![Example GIF](/example.gif)

```python
# Shows currently grown tree. Can be used to experiment with materials.
w.show(material='#', background='i')
```