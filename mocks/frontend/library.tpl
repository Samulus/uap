<!DOCTYPE html>
<html lang="en" xmlns:v-on="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="css/layout.css">
    <link rel="stylesheet" href="css/vital.min.css">
    <title>uap</title>
    <script src="js/vue.js"></script>
</head>
<body>

    <input class="input search" placeholder="Search...">

    <div class="autogrid tabs-block">
        <div id="VUE_view_queue" class="col" v-on:click="viewTab">Queue</div>
        <div id="VUE_view_library" class="col" v-on:click="viewTab">Library</div>
        <div id="VUE_view_settings" class="col" v-on:click="viewTab">Settings</div>
    </div>

    <template id="VUE_queue">
        (Queue Not Implemented)
    </template>

    <template id="VUE_library">
        <table>
            <tbody>
            % for song in library:
            <tr>
                <td>{{song["artist"][0] if "artist" in song else "(none)"}}</td>
                <td>{{song["album"][0] if "album" in song else "(none)"}}</td>
                <td>{{song["title"][0] if "title" in song else "(none)"}}</td>
                <td><button>Enqueue</button></td>
            </tr>
            % end
            </tbody>
        </table>
    </template>

    <template id="VUE_settings">
        (Settings Not Implemented)
    </template>

    <div id="VUE_view">
    </div>

    <script>
        document.getElementById("VUE_view").innerHTML =
        document.getElementById("VUE_library").innerHTML;
    </script>

    <script src="js/bind.js"></script>
</body>
</html>