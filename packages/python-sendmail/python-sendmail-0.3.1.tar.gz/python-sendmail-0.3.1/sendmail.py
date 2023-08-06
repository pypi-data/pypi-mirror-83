# -*- coding: utf-8 -*-
import os
import io
from io import open
import smtplib
from email import generator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.parser import Parser
import mimetypes
import click


def ignore_default_codec_map():
    from email import charset
    _names = list(charset.CODEC_MAP.keys())
    for _name in _names:
        del charset.CODEC_MAP[_name]


def get_content(content, encoding="utf-8"):
    if not content:
        if hasattr(os.sys.stdin, "reconfigure"):
            os.sys.stdin.reconfigure(encoding=encoding)
            content = os.sys.stdin.read()
            return content
        else:
            import codecs
            content = codecs.getreader(encoding)(os.sys.stdin).read()
            return content
    if os.path.exists(content):
        with open(content, "r", encoding=encoding) as fobj:
            return fobj.read()
    return content


def addresses_encode(addresses, charset="utf-8"):
    return ", ".join([address_encode(address, charset) for address in addresses])


def address_encode(value, charset="utf-8"):
    if u"<" in value:
        name, email = value.split(u"<")
        name = name.strip()
        email = email.replace(u">", u"")
    else:
        name = value
        email = value
    return u"{0} <{1}>".format(header_encode(name, charset), email)


def header_encode(value, charset="utf-8"):
    return Header(value, charset).encode()


def get_smtp_service(host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    if ssl:
        smtp_service = smtplib.SMTP_SSL(host, port)
    else:
        smtp_service = smtplib.SMTP(host, port)
    if user and password:
        smtp_service.login(user, password)
    return smtp_service


def get_message_from_eml_content(content):
    parser = Parser()
    return parser.parsestr(content)


def make_message(from_address, to_addresses, content, subject, attachs=None, is_html_content=False, charset="utf-8"):
    message = MIMEMultipart()
    if subject:
        message["Subject"] = header_encode(subject, charset)
    message["From"] = address_encode(from_address, charset)
    message["To"] = addresses_encode(to_addresses, charset)

    if is_html_content:
        main_content = MIMEText(content, "html", charset)
    else:
        main_content = MIMEText(content, "plain", charset)
    message.attach(main_content)

    attachs = attachs or []
    for attach in attachs:
        basename = header_encode(os.path.basename(attach), charset)
        part = None
        with open(attach, "rb") as attach_file:
            part = MIMEApplication(attach_file.read(), Name=basename)
        part.add_header("Content-Disposition", "attachment", filename=basename)
        message.attach(part)

    return message


def makemail(from_address, to_addresses, subject, attach, html, encoding, charset, output, content):
    content = get_content(content, encoding)
    message = make_message(from_address, to_addresses, content, subject, attach, html, charset)
    buffer = io.StringIO()
    gen = generator.Generator(buffer)
    gen.flatten(message)
    if output:
        with open(output, "w") as fobj:
            fobj.write(buffer.getvalue())
    else:
        click.echo(buffer.getvalue())
    return message


def sendmail(from_address, to_addresses, content, subject, attachs=None, is_html_content=False, encoding="utf-8", charset="utf-8", host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    content = get_content(content, encoding)
    smtp_service = get_smtp_service(host, port, ssl, user, password)
    message = make_message(from_address, to_addresses, content, subject, attachs, is_html_content, charset)
    smtp_service.send_message(message)
    smtp_service.quit()


def sendeml(content, encoding="utf-8", host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    content = get_content(content, encoding)
    smtp_service = get_smtp_service(host, port, ssl, user, password)
    message = get_message_from_eml_content(content)
    smtp_service.send_message(message)
    smtp_service.quit()


@click.group()
def main():
    """Sendmail client

Notice:

1. Empty content means read mail content from stdin.
2. If the content argument is a file path, read mail content from the file.
3. Otherwise use the content argument as the mail content.
    """
    pass


@main.command(name="makemail")
@click.option("-f", "--from-address", required=True, help=u"Mail sender, e.g. Name <name@example.com> or name@example.com.")
@click.option("-t", "--to-address", multiple=True, required=True, help=u"Mail recipients, e.g. Name <name@example.com> or name@example.com.")
@click.option("-s", "--subject", help=u"Mail subject")
@click.option("-a", "--attach", multiple=True, required=False, help=u"Mail attachments, allow multiple use.")
@click.option("--html", is_flag=True, help=u"Mail content is HTML format.")
@click.option("-e", "--encoding", default="utf-8", help=u"Encoding of the mail content input.")
@click.option("-c", "--charset", default="utf-8", help=u"Encoding of the mail content output.")
@click.option("-o", "--output", required=False, help=u"Save the .eml file to the given path.")
@click.argument("content", nargs=1, required=False)
def makemail_cmd(from_address, to_address, subject, attach, html, encoding, charset, output, content):
    """Make .eml file.
    """
    ignore_default_codec_map()
    to_addresses = to_address
    makemail(from_address, to_addresses, subject, attach, html, encoding, charset, output, content)


@main.command(name="sendmail")
@click.option("-f", "--from-address", required=True, help=u"Mail sender, e.g. Name <name@example.com> or name@example.com.")
@click.option("-t", "--to-address", multiple=True, required=True, help=u"Mail recipients, e.g. Name <name@example.com> or name@example.com.")
@click.option("-s", "--subject", help=u"Mail subject")
@click.option("-a", "--attach", multiple=True, required=False, help=u"Mail attachments, allow multiple use.")
@click.option("--html", is_flag=True, help=u"Mail content is HTML format.")
@click.option("-e", "--encoding", default="utf-8", help=u"Encoding of the mail content input.")
@click.option("-c", "--charset", default="utf-8", help=u"Encoding of the mail content output.")
@click.option("-h", "--host", default="127.0.0.1", help=u"Mail server address, default to 127.0.0.1.")
@click.option("-p", "--port", default=25, help=u"Mail server port, default to 25. If you are using an ssl server, mostly the port should be 465.")
@click.option("--ssl", is_flag=True, help=u"Mail server using ssl encryption.")
@click.option("-u", "--user", help=u"Mail server login account. Empty user means don't use login.")
@click.option("-P", "--password", help=u"Mail server login password. Empty password means don't use login.")
@click.argument("content", nargs=1, required=False)
def sendmail_cmd(from_address, to_address, subject, attach, html, encoding, charset, host, port, ssl, user, password, content):
    u"""Send mail
    """
    ignore_default_codec_map()
    to_addresses = to_address
    sendmail(from_address, to_addresses, content, subject, attach, html, encoding, charset, host, port, ssl, user, password)


@main.command(name="sendeml")
@click.option("-h", "--host", default="127.0.0.1", help=u"Mail server address, default to 127.0.0.1.")
@click.option("-p", "--port", default=25, help=u"Mail server port, default to 25. If you are using an ssl server, mostly the port should be 465.")
@click.option("--ssl", is_flag=True, help=u"Mail server using ssl encryption.")
@click.option("-u", "--user", help=u"Mail server login account. Empty user means don't use login.")
@click.option("-P", "--password", help=u"Mail server login password. Empty password means don't use login.")
@click.option("-e", "--encoding", default="utf-8", help=u"EML file encoding.")
@click.argument("content", nargs=1, required=False)
def sendeml_cmd(host, port, ssl, user, password, encoding, content):
    u"""Send eml file.
    """
    sendeml(content, encoding, host, port, ssl, user, password)


if __name__ == "__main__":
    main()
