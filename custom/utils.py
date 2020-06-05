import re


def get_tag_properties(tag):
    return {
        prop.group(1): prop.group(2)
        for prop in re.finditer(
            r"([\w-]+)=[\'\"]([^\'\"\r\n]+)[\'\"]", tag, re.M
        )
    }


def assemble_tag(tag_dict):
    for key in tag_dict.keys():
        tag_str = f"<{key} "
        for tag in tag_dict[key]:
            yield tag_str + " ".join(
                f"{k}={v!r}" for k, v in tag.items()
            ) + f">"


def get_name(tag):
    if (m := re.match(r"<\/?([^\r\n\s]+)[^>\r\n]+>", tag)) is not None:
        return m.group(1)
    return ""


def update_style_tag(tag, style_dict={}):
    return update_tag(
        tag,
        {"style": update_style(get_tag_properties(tag)["style"], style_dict)},
    )


def update_style(style, style_dict={}):
    old_dict = dict(x.split(":") for x in style.split(";"))
    old_dict.update({k: str(v) for k, v in style_dict.items()})
    return ";".join(":".join(x) for x in old_dict.items())


def update_tag(tag, new_props={}):
    props = get_tag_properties(tag)
    props.update({k: str(v) for k, v in new_props.items()})
    new_tag = [*assemble_tag({get_name(tag): [props]})][0]
    if tag[-2] == "/":
        new_tag = [*new_tag]
        new_tag.insert(-1, "/")
        new_tag = "".join(new_tag)
    return new_tag
