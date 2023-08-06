<%inherit file="${context['midtpl']}" />

<%
usergroups = {}
for g in user.groups:
    usergroups[g.id] = g.name
%>
<div class="row">
    <div class="${bc['xs']}12 col-sm-6">
        <form action="${submiturl}" method="POST" autocomplete="off">
            
            <input class="form-control" type="text" name="username" placeholder="username" value="${user.username if (user and user.username) else ''}">
            </br>
            %if user.id and user.id >= 0:
            <input class="form-control" type="password" name="currentpassword" placeholder="current password" value="">
            </br>
            %endif
            <input class="form-control" type="password" name="password" placeholder="password" value="" autocomplete="new-password">
            </br>
            <input class="form-control" type="password" name="confirmnewpassword" placeholder="confirm new password" value="" autocomplete="new-password">
            <div class="checkbox">
                <label for="enablecheck">
                    <input id="enablecheck" type="checkbox" value="1" checked="checked" name="enabled"> Enable:
                </label>
            </div>
            <p class="label">Groups</p>
            %for g in allgroups:
                <label class="checkbox-inline">
                    <input name="allgroups" type="checkbox" value="${g.id}" ${"checked" if g.id in usergroups else ""}> ${g.name}
                </label>
            %endfor
            </br>
            <input class="btn btn-success" type="submit" name="submit" value="Apply"/>

            <p class="resultmsg">${msg}</p>
        </form>
    </div>
</div>