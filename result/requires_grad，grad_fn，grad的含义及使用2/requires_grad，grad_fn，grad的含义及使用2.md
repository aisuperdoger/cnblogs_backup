原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522337.html
提交日期：Tue, 26 Jul 2022 11:50:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>对<a href="https://blog.csdn.net/zphuangtang/article/details/112788037">requires_grad，grad_fn，grad的含义及使用</a>进行补充说明，请先看此文章。<br> 本文对grad的含义进行补充说明<br> grad为：当执行完了backward()之后，通过x.grad查看x的梯度值。比如z=f(x,y)，那么<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        x
       
       
        .
       
       
        g
       
       
        r
       
       
        a
       
       
        d
       
       
        =
       
       
        
         
          ∂
         
         
          z
         
        
        
         
          ∂
         
         
          x
         
        
       
       
        
         ∣
        
        
         
          x
         
         
          =
         
         
          a
         
        
       
      
      
       x.grad= \frac{\partial z}{\partial x}|_{x=a}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.8889em; vertical-align: -0.1944em;"></span><span class="mord mathnormal">x</span><span class="mord">.</span><span class="mord mathnormal" style="margin-right: 0.0359em;">g</span><span class="mord mathnormal" style="margin-right: 0.0278em;">r</span><span class="mord mathnormal">a</span><span class="mord mathnormal">d</span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 1.2251em; vertical-align: -0.345em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">x</span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight" style="margin-right: 0.044em;">z</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.345em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mord">∣</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.1514em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="mrel mtight">=</span><span class="mord mathnormal mtight">a</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>，a为x的初始值。</p> 
<p>分析下面代码：</p> 
<pre><code class="prism language-python"><span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> x <span class="token operator">=</span> torch<span class="token punctuation">.</span>ones<span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> requires_grad<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span> <span class="token comment"># 2x2全为1的tensor</span>
<span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> y <span class="token operator">=</span> x <span class="token operator">+</span> <span class="token number">2</span>
<span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> z <span class="token operator">=</span> y <span class="token operator">*</span> y <span class="token operator">*</span> <span class="token number">3</span>
<span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> out <span class="token operator">=</span> z<span class="token punctuation">.</span>mean<span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> <span class="token keyword">print</span><span class="token punctuation">(</span>z<span class="token punctuation">,</span> out<span class="token punctuation">)</span>
tensor<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">[</span><span class="token number">27.</span><span class="token punctuation">,</span> <span class="token number">27.</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">[</span><span class="token number">27.</span><span class="token punctuation">,</span> <span class="token number">27.</span><span class="token punctuation">]</span><span class="token punctuation">]</span><span class="token punctuation">,</span> grad_fn<span class="token operator">=</span><span class="token operator">&lt;</span>MulBackward0<span class="token operator">&gt;</span><span class="token punctuation">)</span> tensor<span class="token punctuation">(</span><span class="token number">27.</span><span class="token punctuation">,</span> grad_fn<span class="token operator">=</span><span class="token operator">&lt;</span>MeanBackward0<span class="token operator">&gt;</span><span class="token punctuation">)</span>
<span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> out<span class="token punctuation">.</span>backward<span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> <span class="token keyword">print</span><span class="token punctuation">(</span>x<span class="token punctuation">.</span>grad<span class="token punctuation">)</span>
tensor<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">[</span><span class="token number">4.5000</span><span class="token punctuation">,</span> <span class="token number">4.5000</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">[</span><span class="token number">4.5000</span><span class="token punctuation">,</span> <span class="token number">4.5000</span><span class="token punctuation">]</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre> 
<p>假设<span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">
     
      
       
        
         x
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  
                   x
                  
                  
                   1
                  
                 
                
               
               
                
                 
                  
                   x
                  
                  
                   2
                  
                 
                
               
              
              
               
                
                 
                  
                   x
                  
                  
                   3
                  
                 
                
               
               
                
                 
                  
                   x
                  
                  
                   4
                  
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  1
                 
                
               
               
                
                 
                  1
                 
                
               
              
              
               
                
                 
                  1
                 
                
               
               
                
                 
                  1
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
       
       
        x=\begin{gathered} \begin{bmatrix} x_1 &amp; x_2 \\ x_3 &amp; x_4 \end{bmatrix} \end{gathered}= \begin{gathered} \begin{bmatrix} 1 &amp; 1 \\ 1 &amp; 1 \end{bmatrix} \end{gathered} 
       
      
     </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.4306em;"></span><span class="mord mathnormal">x</span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">1</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">1</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span></span></span></span></span></span><br> 则<span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">
     
      
       
        
         y
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  
                   y
                  
                  
                   1
                  
                 
                
               
               
                
                 
                  
                   y
                  
                  
                   2
                  
                 
                
               
              
              
               
                
                 
                  
                   y
                  
                  
                   3
                  
                 
                
               
               
                
                 
                  
                   y
                  
                  
                   4
                  
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  
                   
                    x
                   
                   
                    1
                   
                  
                  
                   +
                  
                  
                   2
                  
                 
                
               
               
                
                 
                  
                   
                    x
                   
                   
                    2
                   
                  
                  
                   +
                  
                  
                   2
                  
                 
                
               
              
              
               
                
                 
                  
                   
                    x
                   
                   
                    3
                   
                  
                  
                   +
                  
                  
                   2
                  
                 
                
               
               
                
                 
                  
                   
                    x
                   
                   
                    4
                   
                  
                  
                   +
                  
                  
                   2
                  
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  3
                 
                
               
               
                
                 
                  3
                 
                
               
              
              
               
                
                 
                  3
                 
                
               
               
                
                 
                  3
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
       
       
        y=\begin{gathered} \begin{bmatrix} y_1 &amp; y_2 \\ y_3 &amp; y_4 \end{bmatrix} \end{gathered}= \begin{gathered} \begin{bmatrix} x_1+2 &amp; x_2+2 \\ x_3+2 &amp; x_4+2 \end{bmatrix} \end{gathered}= \begin{gathered} \begin{bmatrix} 3 &amp; 3 \\ 3 &amp; 3 \end{bmatrix} \end{gathered} 
       
      
     </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.625em; vertical-align: -0.1944em;"></span><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord">2</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord">2</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span></span></span></span></span></span><br> <span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">
     
      
       
        
         z
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  
                   z
                  
                  
                   1
                  
                 
                
               
               
                
                 
                  
                   z
                  
                  
                   2
                  
                 
                
               
              
              
               
                
                 
                  
                   z
                  
                  
                   3
                  
                 
                
               
               
                
                 
                  
                   z
                  
                  
                   4
                  
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  
                   3
                  
                  
                   
                    y
                   
                   
                    1
                   
                   
                    2
                   
                  
                 
                
               
               
                
                 
                  
                   3
                  
                  
                   
                    y
                   
                   
                    2
                   
                   
                    2
                   
                  
                 
                
               
              
              
               
                
                 
                  
                   3
                  
                  
                   
                    y
                   
                   
                    3
                   
                   
                    2
                   
                  
                 
                
               
               
                
                 
                  
                   3
                  
                  
                   
                    y
                   
                   
                    3
                   
                   
                    2
                   
                  
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  27
                 
                
               
               
                
                 
                  27
                 
                
               
              
              
               
                
                 
                  27
                 
                
               
               
                
                 
                  27
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
       
       
        z=\begin{gathered} \begin{bmatrix} z_1 &amp; z_2 \\ z_3 &amp; z_4 \end{bmatrix} \end{gathered}= \begin{gathered} \begin{bmatrix} 3y_1^2 &amp; 3y_2^2 \\ 3y_3^2 &amp; 3y_3^2 \end{bmatrix} \end{gathered}= \begin{gathered} \begin{bmatrix} 27&amp; 27 \\ 27 &amp; 27 \end{bmatrix} \end{gathered} 
       
      
     </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.4306em;"></span><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8141em;"><span class="" style="top: -2.4519em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2481em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8141em;"><span class="" style="top: -2.4519em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2481em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8141em;"><span class="" style="top: -2.4519em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2481em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">3</span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8141em;"><span class="" style="top: -2.4519em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2481em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.7em; vertical-align: -1.1em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.6em;"><span class="" style="top: -3.6em;"><span class="pstrut" style="height: 3.45em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">27</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">27</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">27</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">27</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.1em;"><span class=""></span></span></span></span></span></span></span></span></span></span></span></span><br> <span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">
     
      
       
        
         o
        
        
         u
        
        
         t
        
        
         =
        
        
         
          
           
            z
           
           
            1
           
          
          
           +
          
          
           
            z
           
           
            2
           
          
          
           +
          
          
           
            z
           
           
            3
           
          
          
           +
          
          
           
            z
           
           
            4
           
          
         
         
          4
         
        
       
       
        out = \frac{z_1+z_2+z_3+z_4}{4}
       
      
     </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.6151em;"></span><span class="mord mathnormal">o</span><span class="mord mathnormal">u</span><span class="mord mathnormal">t</span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 1.9463em; vertical-align: -0.686em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.2603em;"><span class="" style="top: -2.314em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">4</span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.677em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.2222em;"></span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.044em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.686em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span></span></span></p> 
<p>则<span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">
     
      
       
        
         x
        
        
         .
        
        
         g
        
        
         r
        
        
         a
        
        
         d
        
        
         =
        
        
         
          
           
            
             
              [
             
             
              
               
                
                 
                  
                   
                    
                     ∂
                    
                    
                     o
                    
                    
                     u
                    
                    
                     t
                    
                   
                   
                    
                     ∂
                    
                    
                     
                      x
                     
                     
                      1
                     
                    
                   
                  
                  
                   
                    ∣
                   
                   
                    
                     
                      x
                     
                     
                      1
                     
                    
                    
                     =
                    
                    
                     1
                    
                   
                  
                 
                
               
               
                
                 
                  
                   
                    
                     ∂
                    
                    
                     o
                    
                    
                     u
                    
                    
                     t
                    
                   
                   
                    
                     ∂
                    
                    
                     
                      x
                     
                     
                      2
                     
                    
                   
                  
                  
                   
                    ∣
                   
                   
                    
                     
                      x
                     
                     
                      2
                     
                    
                    
                     =
                    
                    
                     1
                    
                   
                  
                 
                
               
              
              
               
                
                 
                  
                   
                    
                     ∂
                    
                    
                     o
                    
                    
                     u
                    
                    
                     t
                    
                   
                   
                    
                     ∂
                    
                    
                     
                      x
                     
                     
                      3
                     
                    
                   
                  
                  
                   
                    ∣
                   
                   
                    
                     
                      x
                     
                     
                      3
                     
                    
                    
                     =
                    
                    
                     1
                    
                   
                  
                 
                
               
               
                
                 
                  
                   
                    
                     ∂
                    
                    
                     o
                    
                    
                     u
                    
                    
                     t
                    
                   
                   
                    
                     ∂
                    
                    
                     
                      x
                     
                     
                      4
                     
                    
                   
                  
                  
                   
                    ∣
                   
                   
                    
                     
                      x
                     
                     
                      4
                     
                    
                    
                     =
                    
                    
                     1
                    
                   
                  
                 
                
               
              
             
             
              ]
             
            
           
          
         
        
       
       
        x.grad=\begin{gathered} \begin{bmatrix} \frac{\partial out}{\partial x_1}|_{x_1=1} &amp; \frac{\partial out}{\partial x_2}|_{x_2=1} \\ \frac{\partial out}{\partial x_3}|_{x_3=1} &amp; \frac{\partial out}{\partial x_4}|_{x_4=1} \end{bmatrix} \end{gathered} 
       
      
     </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.8889em; vertical-align: -0.1944em;"></span><span class="mord mathnormal">x</span><span class="mord">.</span><span class="mord mathnormal" style="margin-right: 0.0359em;">g</span><span class="mord mathnormal" style="margin-right: 0.0278em;">r</span><span class="mord mathnormal">a</span><span class="mord mathnormal">d</span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 2.9504em; vertical-align: -1.2252em;"></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.7252em;"><span class="" style="top: -3.7252em;"><span class="pstrut" style="height: 3.5752em;"></span><span class="mord"><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.5752em;"><span class="" style="top: -3.6951em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mord">∣</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span><span class="mrel mtight">=</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.3699em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mord">∣</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span><span class="mrel mtight">=</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.0752em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.5752em;"><span class="" style="top: -3.6951em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mord">∣</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span><span class="mrel mtight">=</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span></span></span><span class="" style="top: -2.3699em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mord">∣</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">4</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span><span class="mrel mtight">=</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.0752em;"><span class=""></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top: 0em;"><span class="delimsizing size3">]</span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.2252em;"><span class=""></span></span></span></span></span></span></span></span></span></span></span></span><br> 我们以<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         
          ∂
         
         
          o
         
         
          u
         
         
          t
         
        
        
         
          ∂
         
         
          
           x
          
          
           1
          
         
        
       
       
        
         ∣
        
        
         
          
           x
          
          
           1
          
         
         
          =
         
         
          1
         
        
       
      
      
       \frac{\partial out}{\partial x_1}|_{x_1=1}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.3252em; vertical-align: -0.4451em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mord">∣</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span><span class="mrel mtight">=</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span></span></span></span></span>为例进行说明：</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         
          ∂
         
         
          o
         
         
          u
         
         
          t
         
        
        
         
          ∂
         
         
          
           x
          
          
           1
          
         
        
       
       
        =
       
       
        
         
          ∂
         
         
          o
         
         
          u
         
         
          t
         
        
        
         
          ∂
         
         
          
           z
          
          
           1
          
         
        
       
       
        
         
          ∂
         
         
          
           z
          
          
           1
          
         
        
        
         
          ∂
         
         
          
           y
          
          
           1
          
         
        
       
       
        
         
          ∂
         
         
          
           y
          
          
           1
          
         
        
        
         
          ∂
         
         
          
           x
          
          
           1
          
         
        
       
       
        =
       
       
        
         1
        
        
         4
        
       
       
        6
       
       
        
         y
        
        
         1
        
       
       
        =
       
       
        4.5
       
      
      
       \frac{\partial out}{\partial x_1}=\frac{\partial out}{\partial z_1}\frac{\partial z_1}{\partial y_1}\frac{\partial y_1}{\partial x_1}=\frac{1}{4}6y_1=4.5
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.3252em; vertical-align: -0.4451em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 1.4133em; vertical-align: -0.4811em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8801em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: -0.044em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mathnormal mtight">o</span><span class="mord mathnormal mtight">u</span><span class="mord mathnormal mtight">t</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8962em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: -0.0359em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.4101em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight" style="margin-right: 0.044em;">z</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: -0.044em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4811em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.9322em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.4461em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight" style="margin-right: 0.0556em;">∂</span><span class="mord mtight"><span class="mord mathnormal mtight" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3173em;"><span class="" style="top: -2.357em; margin-left: -0.0359em; margin-right: 0.0714em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 1.1901em; vertical-align: -0.345em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.8451em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">4</span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.345em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord">6</span><span class="mord"><span class="mord mathnormal" style="margin-right: 0.0359em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3011em;"><span class="" style="top: -2.55em; margin-left: -0.0359em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.2778em;"></span></span><span class="base"><span class="strut" style="height: 0.6444em;"></span><span class="mord">4.5</span></span></span></span></span></p> 
<p>从上面我们可以看出来，x的梯度值（x.grad）就是out对x的偏导值。还可以看出，要求out对x的偏导，需要知道out对z的偏导、z对y的偏导、y对x的偏导。我觉得requires_grad设为True的作用就是保存这些偏导信息（也称为梯度信息），比如y的requires_grad设为True，则会保存“y对x的偏导”这个信息。<br> requires_grad()默认为False，但这不意味着我们需要一个一个地去分别给x、y、z、out设置requires_grad=True。因为pytorch中规定：只要某一个输入需要相关梯度值，则输出也需要保存相关梯度信息，这样就保证了这个输入的梯度回传，即我们只需要设置x的requires_grad=True，就可以保证y、z、out的requires_grad=True。</p> 
<p>再看下面一个注意点：</p> 
<pre><code class="prism language-python"><span class="token operator">&gt;&gt;</span><span class="token operator">&gt;</span> <span class="token keyword">print</span><span class="token punctuation">(</span>y<span class="token punctuation">.</span>grad<span class="token punctuation">)</span>
E<span class="token punctuation">:</span>\softwares\anaconda\envs\pytorch\lib\site<span class="token operator">-</span>packages\torch\_tensor<span class="token punctuation">.</span>py<span class="token punctuation">:</span><span class="token number">1013</span><span class="token punctuation">:</span> UserWarning<span class="token punctuation">:</span> The <span class="token punctuation">.</span>grad attribute of a Tensor that <span class="token keyword">is</span> <span class="token keyword">not</span> a leaf Tensor <span class="token keyword">is</span> being accessed<span class="token punctuation">.</span> Its <span class="token punctuation">.</span>grad attribute won't be populated during autograd<span class="token punctuation">.</span>backward<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span> If you indeed want the <span class="token punctuation">.</span>grad field to be populated <span class="token keyword">for</span> a non<span class="token operator">-</span>leaf Tensor<span class="token punctuation">,</span> use <span class="token punctuation">.</span>retain_grad<span class="token punctuation">(</span><span class="token punctuation">)</span> on the non<span class="token operator">-</span>leaf Tensor<span class="token punctuation">.</span> If you access the non<span class="token operator">-</span>leaf Tensor by mistake<span class="token punctuation">,</span> make sure you access the leaf Tensor instead<span class="token punctuation">.</span> See github<span class="token punctuation">.</span>com<span class="token operator">/</span>pytorch<span class="token operator">/</span>pytorch<span class="token operator">/</span>pull<span class="token operator">/</span><span class="token number">30531</span> <span class="token keyword">for</span> more informations<span class="token punctuation">.</span> <span class="token punctuation">(</span>Triggered internally at  aten\src\ATen<span class="token operator">/</span>core<span class="token operator">/</span>TensorBody<span class="token punctuation">.</span>h<span class="token punctuation">:</span><span class="token number">417.</span><span class="token punctuation">)</span>
  <span class="token keyword">return</span> self<span class="token punctuation">.</span>_grad
<span class="token boolean">None</span>
</code></pre> 
<p>无法打印处y.grad，这是因为并不是每个requires_grad()设为True的值都会在backward的时候得到相应的grad。它还必须为leaf。<br> leaf：requires_grad为True的张量(Tensor),如果他们是由用户创建的,则它们是叶张量(leaf Tensor).这意味着它不是运算的结果,因此gra_fn为None。【参考：<a href="https://blog.csdn.net/qq_40206371/article/details/121314373">链接</a>】</p>
                