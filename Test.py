    @safe
    def onDoubleLeftClick(self,event):
        index = event.widget.index("@%s,%s" % (event.x, event.y))
        line, char = index.split(".")
        linestart="{}.0".format(line)
    
        line=int(line)
        Text=event.widget.get("%d.0" % line, "%d.end" % line)
        ccount=int(char)-1
        start=ccount
        end=ccount
        try:
            if Text[start]not in('*','\n','~') and  start<>0:
                while Text[start] not in('*','\n','~') and  start<>-1:
                    start-=1
                if start<>ccount :
                    start+=1
                while Text[end] not in('*','\n','~') and end<>len(Text):
                    end+=1
            else:
                end+=1 
                start+=1
                while Text[end] not in('*','\n','~') and end<>len(Text):
                    end+=1
            event.widget.tag_add("sel", "{}.{}".format(str(line),str(start)), "{}.{}".format(str(line),str(end)))
            event.widget.mark_set(INSERT, "{}.{}".format(str(line),str(end)))
            event.widget.see(INSERT)
            return 'break'
        except:
            pass
            
