# specify the VCL syntax version to use
vcl 4.1;

backend default {
    .host = "webapp";
    .port = "3000";
}
