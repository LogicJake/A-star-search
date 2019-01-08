## A-star-search  
Visually find the shortest path using A* algorithm.   

![demo](https://raw.githubusercontent.com/LogicJake/A-star-search/master/demo.gif)  

### how to run it
Better to use python3
#### install requirements
```
pip install -r requirements.txt
```
#### start
```
python main.py
```
### description
* Green block represents starting block  
* Blue blocks represent obstacle blocks  
* Red block represents finding block  
* Blocks with yellow border are in the close list  
* Blocks with green border are in the open list  
* Arrow inside block points to his parent block  




As you can see in the gif, you should click blocks to set starting block, obstacle blocks and finding block. If you don't know what to do, you can read the title on the screen. You can have zero or more than one obstacle blocks, just click until you think the number of obstacle blocks are enough. And then press space key to choose a finding block.  
  

After you choose all blocks, the search will start. You can press space key to step the search.
