document.addEventListener("adobe_dc_view_sdk.ready", function(){
            var adobeDCView = new AdobeDC.View({clientId: "e3eb34af4932481693d6f87dfb7f0805", divId: "adobe-dc-view"});
            adobeDCView.previewFile({
                content:{location:
                        {url: "https://www.millforma-admin.fr/public/{{path}}" }},
                metaData:{fileName: "{{doc_name}}"}
            }, {embedMode: "IN_LINE"});
        });