<html>
<head>
    <link rel="stylesheet" href="/assets/css/960.css" type="text/css" media="screen" charset="utf-8">
    <link rel="stylesheet" href="/assets/css/main.css" type="text/css" media="screen" charset="utf-8">
</head>
<body>
    <div id="site" class="container_12">
        <div id="navbar" class="grid_12">
            <div id="titles" class="grid_2 alpha">
               <a href="/">Yertle the Turtle</a> 
            </div>
            <div id="mainmenu" class="grid_6">
                <ul>
                    <li>
                        <a href="/about">About</a>
                    </li>
                    <li>
                        <a href="/members">Members</a>
                    </li>
                    <li>
                        <a href="/designs">Designs</a>
                    </li>
                    <li>
                        <a href="/media">Media</a>
                    </li>
                    <li>
                        <a href="/contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
        <?php $uri = $_SERVER['REQUEST_URI'] !=  '/'? $_SERVER['REQUEST_URI'] : "/index" ?>
        <?php $uri = str_replace('.php', '', $uri); ?>
        <?php $page = './pages' . $uri . '.html';?>
        <?php 
            if(file_exists($page)) { 
                include $page; 
            }
            else {
                $page = './pages/error.html';                   
                include $page; 
            }
        ?>
        <div id="footer" class="grid_12 omega">
            <span class="info">Spring 2010 Design Project</span>
        </div>
    </div>
</body>

</html>
