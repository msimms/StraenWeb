// -*- coding: utf-8 -*-
// 
// MIT License
// 
// Copyright (c) 2018 Mike Simms
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

function set_background_style(root_url, background_id)
{
    let section = document.getElementById(background_id);
    let img_index = Math.floor(Math.random() * 7) + 1;
    let img_str = 'url("' + root_url + '/images/main_background' + img_index + '.jpg")';
    section.style.backgroundImage = img_str;
}

function unix_time_to_local_string(unix_time)
{
    let date = new Date(unix_time * 1000);
    return date.toLocaleString();
}

function unix_time_to_local_date_string(unix_time)
{
    let date = new Date(unix_time * 1000);
    return date.toLocaleDateString();
}

function unix_time_to_iso_time(unix_time)
{
    let date = new Date(unix_time * 1000);
    return date.toISOString();
}

function serialize_to_url_params(dict)
{
    let str = [];
    for (let p in dict)
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dict[p]));
    return str.join("&");
}

function serialize_to_json(list)
{
    let str = [];
    for (let i = 0; i < list.length; ++i)
        for (let key in list[i])
            str.push(JSON.stringify(key) + ": " + JSON.stringify(list[i][key]));
    json_str = "{" + str.join(",") + "}"
    return json_str
}

/// @function Sends an HTTP GET request and waits for the response.
function send_get_request(url, result_text)
{
    let result = false;

    let xml_http = new XMLHttpRequest();
    let content_type = "application/json; charset=utf-8";

    xml_http.open("GET", url, false);
    xml_http.setRequestHeader('Content-Type', content_type);
    xml_http.onreadystatechange = function()
    {
        if (xml_http.readyState == XMLHttpRequest.DONE)
        {
            result_text.value = xml_http.responseText;
        }
        result = (xml_http.status == 200);
    }
    xml_http.send();
    return result;
}

/// @function Sends an HTTP GET request and waits for the response.
function send_get_request_async(url, callback)
{
    let xml_http = new XMLHttpRequest();
    let content_type = "application/json; charset=utf-8";

    xml_http.open("GET", url, true);
    xml_http.setRequestHeader('Content-Type', content_type);
    xml_http.onreadystatechange = function()
    {
        if (xml_http.readyState == XMLHttpRequest.DONE)
        {
            callback(xml_http.status, xml_http.responseText);
        }
    }
    xml_http.send();
}

/// @function Sends an HTTP POST request and waits for the response.
function send_post_request(url, params, result_text)
{
    let result = false;

    let xml_http = new XMLHttpRequest();
    let content_type = "application/json; charset=utf-8";

    xml_http.open("POST", url, false);
    xml_http.setRequestHeader('Content-Type', content_type);
    xml_http.onreadystatechange = function()
    {
        if (xml_http.readyState == XMLHttpRequest.DONE)
        {
            result_text.value = xml_http.responseText;
        }
        result = (xml_http.status == 200);
    }
    json_data = serialize_to_json(params);
    xml_http.send(json_data);
    return result;
}

function create_local_file(data, filename, type)
{
    let file = new Blob([data], {type: type});

    if (window.navigator.msSaveOrOpenBlob)
    {
        window.navigator.msSaveOrOpenBlob(file, filename);
    }
    else
    {
        let a = document.createElement("a"),
            url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);  
        }, 0); 
    }
}

function add_number_entry_node(div, name)
{
    let label = document.createTextNode(name + ": ");
    div.appendChild(label);

    let value = document.createElement("input");
    value.name = name;
    value.setAttribute("id", name);
    value.setAttribute("type", "number");
    value.setAttribute("value", 0.0);
    div.appendChild(value);

    let br = document.createElement("br");
    div.appendChild(br);
}

function add_text_entry_node(div, name)
{
    let label = document.createTextNode(name + ": ");
    div.appendChild(label);

    let value = document.createElement("input");
    value.name = name;
    value.setAttribute("id", name);
    value.setAttribute("type", "text");
    value.setAttribute("value", "");
    div.appendChild(value);

    let br = document.createElement("br");
    div.appendChild(br);
}
